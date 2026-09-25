## Test: Test_AwsObjectStorage_ListObjects_Minimal

**Status**: ✗ Failed

### Output:
```
STDERR:
2026-09-25 09:59:18,838 - extension.py INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 09:59:18,838 - extension.py INFO: Action requested: List Objects
2026-09-25 09:59:18,838 - list_objects.py INFO: Starting list_objects action
2026-09-25 09:59:18,838 - utility.py ERROR: S3 ClientError — code: InvalidAccessKeyId, message: The AWS Access Key Id you provided does not exist in our records.

EXTENSION:
{"exit_code": 1, "status_description": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records."}
```

### Notes:
- Known failure: placeholder AWS credentials (test-placeholder-key) rejected by AWS.
- Extension dispatched correctly to List Objects action and reached AWS API before failing.
