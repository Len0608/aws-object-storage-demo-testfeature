## Test: Test_AwsObjectStorage_UploadFile_SubFolder

**Status**: ✗ Failed

### Output:
```
STDERR: Local file not found: /home/agent/ue-test-data/test-upload.txt
EXTENSION: {"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "errors": [{"type": "LocalFileNotFoundError"}]}
```

### Notes:
- Extension loaded and dispatched correctly to Upload File action
- Failed because test file /home/agent/ue-test-data/test-upload.txt does not exist on agent host
- Target S3 key was uploads/subdir/test-upload.txt
