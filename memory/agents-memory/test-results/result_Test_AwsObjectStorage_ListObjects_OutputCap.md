## Test: Test_AwsObjectStorage_ListObjects_OutputCap

**Status**: ✗ Failed

### Output:
```
STDERR: S3 ClientError — code: InvalidAccessKeyId, message: The AWS Access Key Id you provided does not exist in our records.
EXTENSION: {"exit_code": 1, "status_description": "S3 API error: InvalidAccessKeyId: ...", "errors": [{"type": "S3ApiError"}]}
```

### Notes:
- Extension loaded and dispatched correctly to List Objects action
- Failed at AWS API call — InvalidAccessKeyId (placeholder credentials)
- Known failure: test-placeholder-key is not a valid AWS key
