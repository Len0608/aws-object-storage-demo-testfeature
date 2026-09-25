## Issue: Test_AwsObjectStorage_ListObjects_Minimal

**Status**: ✗ Failed

### Expected:
List objects in S3 bucket ue-test-aws-s3-demo in us-east-1.

### STDOUT:
[empty]

### STDERR:
2026-09-25 09:59:18,838 - extension.py INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 09:59:18,838 - extension.py INFO: Action requested: List Objects
2026-09-25 09:59:18,838 - list_objects.py INFO: Starting list_objects action
2026-09-25 09:59:18,838 - list_objects.py INFO: Input validation passed
2026-09-25 09:59:18,838 - list_objects.py INFO: Initialising S3 client for region: us-east-1
2026-09-25 09:59:19,336 - utility.py ERROR: S3 ClientError — code: InvalidAccessKeyId, message: The AWS Access Key Id you provided does not exist in our records.
2026-09-25 09:59:19,337 - extension.py ERROR: Execution error: S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{"exit_code": 1, "status_description": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.", "errors": [{"type": "S3ApiError", "message": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.", "exit_code": 1}]}

### Notes:
- Known failure: placeholder AWS credentials used (test-placeholder-key). Extension code ran correctly and handled the error properly.
