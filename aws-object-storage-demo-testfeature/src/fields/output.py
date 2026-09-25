"""OutputFields dataclass for real-time UI updates."""

from dataclasses import dataclass, asdict
from typing import Optional
from universal_extension import ui
from fields.types import Text


@dataclass
class OutputFields:
    """Real-time output fields for UAC UI updates.

    Maps to the Output Only fields defined in template.json:
      - status  (Text Field 5) — short action summary shown in the task list view
      - result  (Text Field 6) — action-specific supporting detail on success

    These fields sync with the UAC UI in real-time during execution and are
    preserved across re-runs via InputFields.previous_output.
    """

    # Short action summary: populated on success or failure
    # Examples:
    #   "Success: Listed 42 objects in my-demo-bucket"
    #   "Error: Authentication failed — InvalidClientTokenId"
    status: Optional[Text] = None

    # Action-specific detail: populated on success
    # Examples:
    #   "42 objects found"
    #   'ETag: "d41d8cd98f00b204e9800998ecf8427e"'
    result: Optional[Text] = None

    def update(self, **fields):
        """Update fields and sync with UAC UI in real-time.

        Args:
            **fields: Field names and string values to update.
                      String values are automatically wrapped in Text.
        """
        for field_name, field_value in fields.items():
            if hasattr(self, field_name):
                if isinstance(field_value, str):
                    field_value = Text(field_value)
                setattr(self, field_name, field_value)
        ui.update_output_fields(fields)

    def to_dict(self) -> dict:
        """Get current fields as a dictionary.

        Returns:
            Dict mapping field names to their string values;
            None fields are excluded.
        """
        result = {}
        for k, v in asdict(self).items():
            if v is not None:
                result[k] = v.value if isinstance(v, Text) else v
        return result

    def clear(self):
        """Reset all fields to None."""
        self.status = None
        self.result = None
