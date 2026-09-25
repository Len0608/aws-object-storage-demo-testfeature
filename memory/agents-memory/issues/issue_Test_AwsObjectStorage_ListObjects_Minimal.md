## Issue: Test_AwsObjectStorage_ListObjects_Minimal

**Status**: ✗ Failed

### Expected:
List all objects in bucket ue-test-aws-s3-demo; expect at least one object key in output

### STDOUT:
[empty]

### STDERR:
2026-09-25 10:18:xx - list_objects.py INFO: Starting list_objects action
2026-09-25 10:18:xx - utility.py ERROR: S3 ClientError — code: InvalidAccessKeyId, message: The AWS Access Key Id you provided does not exist in our records.
2026-09-25 10:18:xx - extension.py ERROR: Execution error: S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{"exit_code": 1, "status_description": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.", "errors": [{"type": "S3ApiError", "message": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.", "exit_code": 1}]}
