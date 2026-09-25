## Test: Test_AwsObjectStorage_UploadFile_RootKey

**Status**: ✗ Failed

### Output:
```
STDERR: Local file not found: /home/agent/ue-test-data/test-upload.txt
EXTENSION: {"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt"}
```

### Notes:
- Extension loaded and dispatched correctly to Upload File action
- Failed because test file /home/agent/ue-test-data/test-upload.txt does not exist on agent host
- Tests root-level S3 object key (no path prefix)
