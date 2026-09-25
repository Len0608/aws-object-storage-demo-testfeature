"""List Objects action — retrieves and displays all objects in an S3 bucket."""

import logging
import os
import sys
from typing import Any, Dict, List

from tabulate import tabulate

from actions.output import ActionOutput
from exceptions import ValidationError
from fields.input import InputFields
from fields.output import OutputFields
from manager import ExtensionManager
from utility import S3Client, format_size

logger = logging.getLogger("UNV")
extension_manager = ExtensionManager()

# Default cap when UE_MAX_OUTPUT_RECORDS is not set or is not a valid integer
_DEFAULT_MAX_RECORDS = 100


def list_objects(input_data: InputFields) -> ActionOutput:
    """List all objects in the specified S3 bucket and print a formatted table.

    Execution flow:
      1. Validate required inputs.
      2. Read UE_MAX_OUTPUT_RECORDS cap from environment.
      3. Initialise S3Client.
      4. Retrieve all objects with pagination via S3Client.list_objects().
      5. Apply output cap.
      6. Format object records.
      7. Print STDOUT table (rounded_outline).
      8. Emit STDERR warning if truncated.
      9. Populate OutputFields (status, result).
      10. Return ActionOutput with structured result data.

    Args:
        input_data: Validated input fields from UAC.

    Returns:
        ActionOutput containing bucket listing metadata and object records.

    Raises:
        ValidationError:       On missing or empty required input fields.
        AuthenticationError:   On invalid AWS credentials.
        AuthorizationError:    On insufficient IAM permissions.
        BucketNotFoundError:   On non-existent bucket.
        ConnectionError:       On network-level failures.
        S3ApiError:            On any other S3 API error.
    """
    logger.info("Starting list_objects action")
    logger.debug(
        "Input: action=%s, aws_region=%s, bucket_name=%s",
        input_data.action.value if input_data.action else None,
        input_data.aws_region.value if input_data.aws_region else None,
        input_data.bucket_name.value if input_data.bucket_name else None,
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

    aws_region: str = input_data.aws_region.value
    bucket_name: str = input_data.bucket_name.value

    logger.info("Input validation passed")

    # ------------------------------------------------------------------
    # Step 2: Read UE_MAX_OUTPUT_RECORDS from environment
    # ------------------------------------------------------------------
    cap = _DEFAULT_MAX_RECORDS
    env_val = os.environ.get("UE_MAX_OUTPUT_RECORDS")
    if env_val is not None:
        try:
            cap = int(env_val)
            logger.debug("UE_MAX_OUTPUT_RECORDS=%d (from environment)", cap)
        except ValueError:
            logger.warning(
                "UE_MAX_OUTPUT_RECORDS='%s' is not a valid integer; using default %d",
                env_val,
                _DEFAULT_MAX_RECORDS,
            )
            cap = _DEFAULT_MAX_RECORDS
    else:
        logger.debug("UE_MAX_OUTPUT_RECORDS not set; using default %d", cap)

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
    # Step 4: Retrieve all objects with pagination
    # ------------------------------------------------------------------
    logger.info("Retrieving objects from bucket: %s", bucket_name)
    all_objects, total_object_count = s3.list_objects(bucket_name)
    logger.info("Total objects in bucket: %d", total_object_count)

    # ------------------------------------------------------------------
    # Step 5: Apply output cap
    # ------------------------------------------------------------------
    if total_object_count > cap:
        truncated = True
        display_objects = all_objects[:cap]
        logger.warning(
            "Output capped at %d; bucket contains %d objects", cap, total_object_count
        )
    else:
        truncated = False
        display_objects = all_objects

    returned_object_count = len(display_objects)
    logger.debug(
        "returned_object_count=%d, truncated=%s", returned_object_count, truncated
    )

    # ------------------------------------------------------------------
    # Step 6: Format object records for STDOUT table and Extension Output
    # ------------------------------------------------------------------
    table_rows: List[List[str]] = []
    output_records: List[Dict[str, Any]] = []

    for obj in display_objects:
        key: str = obj["key"]
        size_str: str = format_size(obj["size_bytes"])
        last_modified_dt = obj["last_modified"]
        last_modified_str: str = last_modified_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        table_rows.append([key, size_str, last_modified_str])
        output_records.append(
            {
                "key": key,
                "size": size_str,
                "last_modified": last_modified_str,
            }
        )

    logger.debug("Formatted %d object record(s) for display", len(table_rows))

    # ------------------------------------------------------------------
    # Step 7: Print STDOUT table
    # ------------------------------------------------------------------
    table_str = tabulate(
        table_rows,
        headers=["Key", "Size", "Last Modified"],
        tablefmt="rounded_outline",
    )
    print(table_str)

    if truncated:
        print(
            "NOTE: Output capped at %d objects. Total objects in bucket: %d."
            % (cap, total_object_count)
        )

    # ------------------------------------------------------------------
    # Step 8: Emit STDERR warning if truncated
    # ------------------------------------------------------------------
    if truncated:
        print(
            "WARNING: Bucket contains %d objects; output capped at %d by UE_MAX_OUTPUT_RECORDS"
            % (total_object_count, cap),
            file=sys.stderr,
        )

    # ------------------------------------------------------------------
    # Step 9: Populate OutputFields (real-time UI update)
    # ------------------------------------------------------------------
    output_fields = OutputFields()
    output_fields.update(
        status="Success: Listed %d objects in %s" % (returned_object_count, bucket_name),
        result="%d objects found" % returned_object_count,
    )
    logger.debug("OutputFields updated with status and result")

    # ------------------------------------------------------------------
    # Step 10: Return ActionOutput
    # ------------------------------------------------------------------
    logger.info(
        "list_objects action completed — returned %d of %d object(s), truncated=%s",
        returned_object_count,
        total_object_count,
        truncated,
    )

    return ActionOutput(
        bucket=bucket_name,
        total_object_count=total_object_count,
        returned_object_count=returned_object_count,
        truncated=truncated,
        objects=output_records,
    )
