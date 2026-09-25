"""Upload File action — uploads a local file to an S3 bucket."""

import logging
import os

from actions.output import ActionOutput
from exceptions import LocalFileNotFoundError, ValidationError
from fields.input import InputFields
from fields.output import OutputFields
from manager import ExtensionManager
from utility import S3Client

logger = logging.getLogger("UNV")
extension_manager = ExtensionManager()


def upload_file(input_data: InputFields) -> ActionOutput:
    """Upload a local file from the agent host to the specified S3 bucket.

    Execution flow:
      1. Validate required inputs.
      2. Validate local file existence on the agent host filesystem.
      3. Initialise S3Client.
      4. Upload file using put_object via context manager.
      5. Construct output values (filename, s3_uri, etag).
      6. Print STDOUT confirmation.
      7. Populate OutputFields (status, result).
      8. Return ActionOutput with structured result data.

    Args:
        input_data: Validated input fields from UAC.

    Returns:
        ActionOutput containing s3_uri and etag from the upload response.

    Raises:
        ValidationError:         On missing or empty required input fields.
        LocalFileNotFoundError:  When the local file does not exist or is not a file.
        AuthenticationError:     On invalid AWS credentials.
        AuthorizationError:      On insufficient IAM permissions.
        BucketNotFoundError:     On non-existent bucket.
        ConnectionError:         On network-level failures.
        S3ApiError:              On any other S3 API error.
    """
    logger.info("Starting upload_file action")
    logger.debug(
        "Input: action=%s, aws_region=%s, bucket_name=%s, local_file=%s, s3_object_key=%s",
        input_data.action.value if input_data.action else None,
        input_data.aws_region.value if input_data.aws_region else None,
        input_data.bucket_name.value if input_data.bucket_name else None,
        input_data.local_file.value if input_data.local_file else None,
        input_data.s3_object_key.value if input_data.s3_object_key else None,
    )

    # ------------------------------------------------------------------
    # Step 1: Validate required inputs
    # ------------------------------------------------------------------
    if not input_data.aws_credentials:
        raise ValidationError("aws_credentials is required")
    if not input_data.aws_credentials.user:
        raise ValidationError("aws_credentials: AWS Access Key ID (user) is required")
    if not input_data.aws_credentials.password:
        raise ValidationError("aws_credentials: AWS Secret Access Key (password) is required")
    if not input_data.aws_region or not input_data.aws_region.value:
        raise ValidationError("aws_region is required and must not be empty")
    if not input_data.bucket_name or not input_data.bucket_name.value:
        raise ValidationError("bucket_name is required and must not be empty")
    if not input_data.local_file or not input_data.local_file.value:
        raise ValidationError("local_file is required when action is 'Upload File'")
    if not input_data.s3_object_key or not input_data.s3_object_key.value:
        raise ValidationError("s3_object_key is required when action is 'Upload File'")

    aws_region: str = input_data.aws_region.value
    bucket_name: str = input_data.bucket_name.value
    local_file: str = input_data.local_file.value
    s3_object_key: str = input_data.s3_object_key.value

    logger.info("Input validation passed")

    # ------------------------------------------------------------------
    # Step 2: Validate local file existence
    # ------------------------------------------------------------------
    logger.info("Checking local file existence: %s", local_file)
    if not os.path.isfile(local_file):
        logger.error("Local file not found: %s", local_file)
        raise LocalFileNotFoundError(local_file)

    logger.debug("Local file exists and is a regular file: %s", local_file)

    # ------------------------------------------------------------------
    # Step 3: Initialise S3 client
    # ------------------------------------------------------------------
    logger.info("Initialising S3 client for region: %s", aws_region)
    s3 = S3Client(
        access_key_id=input_data.aws_credentials.user,
        secret_access_key=input_data.aws_credentials.password,
        region_name=aws_region,
    )

    # ------------------------------------------------------------------
    # Step 4: Upload file using a context manager to guarantee cleanup
    # ------------------------------------------------------------------
    logger.info(
        "Opening local file for upload: %s -> s3://%s/%s",
        local_file,
        bucket_name,
        s3_object_key,
    )
    with open(local_file, "rb") as file_handle:
        etag: str = s3.upload_file(
            bucket_name=bucket_name,
            s3_object_key=s3_object_key,
            file_handle=file_handle,
        )

    logger.info("File upload complete. ETag: %s", etag)

    # ------------------------------------------------------------------
    # Step 5: Construct output values
    # ------------------------------------------------------------------
    filename: str = os.path.basename(local_file)
    s3_uri: str = "s3://%s/%s" % (bucket_name, s3_object_key)

    logger.debug("filename=%s, s3_uri=%s, etag=%s", filename, s3_uri, etag)

    # ------------------------------------------------------------------
    # Step 6: Print STDOUT confirmation
    # ------------------------------------------------------------------
    print("Uploaded %s to %s (ETag: %s)" % (filename, s3_uri, etag))

    # ------------------------------------------------------------------
    # Step 7: Populate OutputFields (real-time UI update)
    # ------------------------------------------------------------------
    output_fields = OutputFields()
    output_fields.update(
        status="Success: Uploaded %s to %s" % (filename, s3_uri),
        result="ETag: %s" % etag,
    )
    logger.debug("OutputFields updated with status and result")

    # ------------------------------------------------------------------
    # Step 8: Return ActionOutput
    # ------------------------------------------------------------------
    logger.info("upload_file action completed — s3_uri=%s", s3_uri)

    return ActionOutput(
        s3_uri=s3_uri,
        etag=etag,
    )
