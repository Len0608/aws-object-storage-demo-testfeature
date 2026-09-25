"""InputFields dataclass for input parsing and validation."""

from dataclasses import dataclass
from dataclasses import fields as dataclass_fields
from dataclasses import asdict
from pathlib import Path
from typing import Optional, Union, get_type_hints, get_origin, get_args
from fields.output import OutputFields
from fields.types import (
    Text,
    Integer,
    Float,
    Boolean,
    SingleChoice,
    MultiChoice,
    Credential,
    Script,
    Array,
)
from exceptions import DataValidationError
from manager import ExtensionManager

extension_manager = ExtensionManager()


@dataclass
class InputFields:
    """Input fields from UAC with validation.

    Fields map directly to template.json field names.
    All user-defined fields are Optional — UAC Controller enforces
    required field validation before the extension starts.

    Output-only fields (status, result) are NOT included here;
    they live in OutputFields.
    """

    # Choice field — selects the S3 operation to perform
    action: Optional[SingleChoice] = None

    # Credential field — AWS IAM access key (user = key ID, password = secret)
    aws_credentials: Optional[Credential] = None

    # Text fields — always visible and required
    aws_region: Optional[Text] = None
    bucket_name: Optional[Text] = None

    # Text fields — visible and required only when action = "Upload File"
    local_file: Optional[Text] = None
    s3_object_key: Optional[Text] = None

    # Previous run output (auto-populated for re-runs)
    previous_output: Optional[OutputFields] = None

    # Skip validation flag (internal use only)
    _skip_validation: bool = False

    @staticmethod
    def preprocess_fields(fields: dict) -> dict:
        """Preprocess raw UAC fields before creating InputFields.

        Converts raw UAC values to wrapper type instances:
        1. Filters out flattened credential fields (containing dots)
        2. Wraps values in appropriate wrapper types based on field type hints
        3. Extracts previous OutputFields if present (from re-runs)

        Args:
            fields: Raw field dict received from UAC

        Returns:
            Processed dict suitable for InputFields(**processed)
        """
        processed = {}
        previous_output_data = {}

        # Get all OutputFields field names for detection
        output_field_names = {f.name for f in dataclass_fields(OutputFields)}

        # Get type hints to detect wrapper types
        type_hints = get_type_hints(InputFields)

        # Map field names to their wrapper types
        field_wrapper_types = {}
        for field_name, field_type in type_hints.items():
            base_type = field_type
            if get_origin(field_type) is Union:
                args = get_args(field_type)
                non_none_args = [arg for arg in args if arg is not type(None)]
                if non_none_args:
                    base_type = non_none_args[0]
            field_wrapper_types[field_name] = base_type

        for key, value in fields.items():
            # Skip flattened credential fields (e.g., "aws_credentials.token")
            if "." in key:
                continue

            # Check if this field belongs to OutputFields (previous run data)
            if key in output_field_names:
                previous_output_data[key] = value
                continue

            # Pass through None values
            if value is None:
                processed[key] = value
                continue

            # Get the wrapper type for this field
            wrapper_type = field_wrapper_types.get(key)

            # Convert to appropriate wrapper type
            if wrapper_type == SingleChoice:
                if isinstance(value, list):
                    value = SingleChoice(_values=value)
                else:
                    value = SingleChoice(_values=[value])

            elif wrapper_type == MultiChoice:
                if isinstance(value, list):
                    value = MultiChoice(values=value)
                else:
                    value = MultiChoice(values=[value])

            elif wrapper_type == Script:
                if isinstance(value, str):
                    value = Script(path=Path(value))

            elif wrapper_type == Credential:
                if isinstance(value, dict):
                    value = Credential.from_dict(value)

            elif wrapper_type == Text:
                if isinstance(value, str):
                    value = Text(value=value)

            elif wrapper_type == Integer:
                if isinstance(value, int):
                    value = Integer(value=value)

            elif wrapper_type == Float:
                if isinstance(value, (int, float)):
                    value = Float(value=float(value))

            elif wrapper_type == Boolean:
                if isinstance(value, bool):
                    value = Boolean(value=value)

            elif wrapper_type == Array:
                if isinstance(value, list):
                    value = Array(pairs=value)

            processed[key] = value

        # If previous output fields were found, create an OutputFields instance
        if previous_output_data:
            for k, v in previous_output_data.items():
                if isinstance(v, str):
                    previous_output_data[k] = Text(value=v)
            processed["previous_output"] = OutputFields(**previous_output_data)

        return processed

    def to_dict(self) -> dict:
        """Convert to dict, unwrapping wrapper types and excluding internal fields.

        Returns:
            Dict with unwrapped field values, excluding _skip_validation
            and None previous_output.
        """
        data = asdict(self)
        result = {}
        for key, value in data.items():
            if key == "_skip_validation":
                continue
            if key == "previous_output" and value is None:
                continue
            if isinstance(value, dict):
                if "_values" in value:  # SingleChoice
                    result[key] = value["_values"]
                elif "values" in value and len(value) == 1:  # MultiChoice
                    result[key] = value["values"]
                elif "value" in value and len(value) == 1:  # Text, Integer, Float, Boolean
                    result[key] = value["value"]
                elif "path" in value:  # Script
                    result[key] = str(value["path"])
                elif "pairs" in value:  # Array
                    result[key] = value["pairs"]
                elif "user" in value:  # Credential
                    result[key] = value
                else:
                    result[key] = value
            else:
                result[key] = value
        return result

    def __post_init__(self):
        """Validate all fields after initialization."""
        if self._skip_validation:
            return

        self._validate_action()
        self._validate_aws_credentials()
        self._validate_aws_region()
        self._validate_bucket_name()
        self._validate_local_file()
        self._validate_s3_object_key()

        if extension_manager.has_errors():
            raise DataValidationError(
                f"Validation failed with {extension_manager.error_count()} error(s)"
            )

    def _validate_action(self):
        """Validate action field.

        Must be one of the defined S3 operations.
        """
        if self.action is not None:
            valid_actions = ["List Objects", "Upload File"]
            if self.action.value not in valid_actions:
                exc = DataValidationError(
                    f"Invalid action '{self.action.value}'. "
                    f"Valid actions: {', '.join(valid_actions)}"
                )
                extension_manager.add_error(exc, field="action", value=self.action.value)

    def _validate_aws_credentials(self):
        """Validate aws_credentials field.

        Both user (Access Key ID) and password (Secret Access Key) must be non-empty.
        """
        if self.aws_credentials is not None:
            if not self.aws_credentials.user:
                exc = DataValidationError(
                    "aws_credentials: AWS Access Key ID (user) is required"
                )
                extension_manager.add_error(exc, field="aws_credentials")
            if not self.aws_credentials.password:
                exc = DataValidationError(
                    "aws_credentials: AWS Secret Access Key (password) is required"
                )
                extension_manager.add_error(exc, field="aws_credentials")

    def _validate_aws_region(self):
        """Validate aws_region field.

        Must be a non-empty string when provided.
        """
        if self.aws_region is not None and self.aws_region.value == "":
            exc = DataValidationError("aws_region is required and must not be empty")
            extension_manager.add_error(exc, field="aws_region")

    def _validate_bucket_name(self):
        """Validate bucket_name field.

        Must be a non-empty string when provided.
        """
        if self.bucket_name is not None and self.bucket_name.value == "":
            exc = DataValidationError("bucket_name is required and must not be empty")
            extension_manager.add_error(exc, field="bucket_name")

    def _validate_local_file(self):
        """Validate local_file field.

        Only validated when action is 'Upload File'.
        UAC sends empty strings for hidden fields — check for both None and empty.
        """
        if self.action and self.action.value == "Upload File":
            if not self.local_file or self.local_file.value == "":
                exc = DataValidationError(
                    "local_file is required when action is 'Upload File'"
                )
                extension_manager.add_error(exc, field="local_file")

    def _validate_s3_object_key(self):
        """Validate s3_object_key field.

        Only validated when action is 'Upload File'.
        UAC sends empty strings for hidden fields — check for both None and empty.
        """
        if self.action and self.action.value == "Upload File":
            if not self.s3_object_key or self.s3_object_key.value == "":
                exc = DataValidationError(
                    "s3_object_key is required when action is 'Upload File'"
                )
                extension_manager.add_error(exc, field="s3_object_key")
