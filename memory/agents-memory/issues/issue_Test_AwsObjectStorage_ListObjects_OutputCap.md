## Issue: Test_AwsObjectStorage_ListObjects_OutputCap

**Status**: ✗ Failed

### Expected:
List objects with UE_MAX_OUTPUT_RECORDS=2; expect at most 2 objects returned

### STDOUT:
[empty]

### STDERR:
2026-09-25 10:18:xx - list_objects.py INFO: Starting list_objects action
2026-09-25 10:18:xx - utility.py ERROR: S3 ClientError — code: InvalidAccessKeyId, message: The AWS Access Key Id you provided does not exist in our records.
2026-09-25 10:18:xx - extension.py ERROR: Execution error: S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{"exit_code": 1, "status_description": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.", "errors": [{"type": "S3ApiError", "message": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.", "exit_code": 1}]}
