## Issue: Test_AwsObjectStorage_ListObjects_AfterUpload_WithCap

**Status**: ✗ Failed

### Expected:
List objects in S3 bucket after upload with output cap applied.

### STDOUT:
[empty]

### STDERR:
2026-09-25 10:08:22,492 - extension.py[63] INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 10:08:22,493 - extension.py[70] INFO: Action requested: List Objects
2026-09-25 10:08:22,493 - list_objects.py[78] INFO: Input validation passed
ERROR: S3 ClientError — code: InvalidAccessKeyId, message: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{"exit_code": 1, "status_description": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.", "errors": [{"type": "S3ApiError", "exit_code": 1}]}
