## Test: Test_AwsObjectStorage_ListObjects_OutputCap

**Status**: ✗ Failed

### Output:
```
STDERR: S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.
EXTENSION: {"exit_code": 1, "status_description": "S3 API error: InvalidAccessKeyId: ..."}
```

### Notes:
- Known failure: placeholder AWS credentials (test-placeholder-key) rejected by AWS.
