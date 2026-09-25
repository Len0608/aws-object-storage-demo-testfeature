## Test: Test_AwsObjectStorage_ListObjects_Minimal

**Status**: ✗ Failed

### Output:
```
STDERR:
2026-09-25 10:06:19,806 - extension.py[63] INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 10:06:19,806 - extension.py[70] INFO: Action requested: List Objects
2026-09-25 10:06:20,296 - utility.py[229] ERROR: S3 ClientError — code: InvalidAccessKeyId, message: The AWS Access Key Id you provided does not exist in our records.
2026-09-25 10:06:20,296 - extension.py[90] ERROR: Execution error: S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.

EXTENSION:
{"exit_code": 1, "status_description": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.", "errors": [{"type": "S3ApiError"}]}
```

### Notes:
- Extension loaded and dispatched correctly to List Objects action
- Reached AWS API call — failed with InvalidAccessKeyId (placeholder credentials)
- Known failure: test-placeholder-key credentials are not valid AWS credentials
