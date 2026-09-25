## Issue: Test_AwsObjectStorage_ListObjects_AfterUpload

**Status**: ✗ Failed

### Expected:
List objects in S3 bucket after a prior upload to confirm object presence.

### STDOUT:
[empty]

### STDERR:
2026-09-25 10:00:22 - extension.py INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 10:00:22 - extension.py INFO: Action requested: List Objects
2026-09-25 10:00:22 - utility.py ERROR: S3 ClientError — code: InvalidAccessKeyId, message: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{"exit_code": 1, "status_description": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records."}

### Notes:
- Known failure: placeholder AWS credentials rejected by AWS.
