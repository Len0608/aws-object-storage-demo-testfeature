## Issue: Test_AwsObjectStorage_ListObjects_AfterUpload_WithCap

**Status**: ✗ Failed

### Expected:
List objects in S3 bucket with output cap after a prior upload.

### STDOUT:
[empty]

### STDERR:
S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{"exit_code": 1, "status_description": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records."}

### Notes:
- Known failure: placeholder AWS credentials (test-placeholder-key) rejected by AWS.
