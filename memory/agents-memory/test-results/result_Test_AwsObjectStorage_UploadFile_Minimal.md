## Test: Test_AwsObjectStorage_UploadFile_Minimal

**Status**: ✗ Failed

### Output:
```
STDERR: Local file not found: /home/agent/ue-test-data/test-upload.txt
EXTENSION: {"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "errors": [{"type": "LocalFileNotFoundError"}]}
```

### Notes:
- Extension loaded and dispatched correctly to Upload File action
- Input validation passed
- Failed because test file /home/agent/ue-test-data/test-upload.txt does not exist on agent host
- Also uses placeholder credentials — would fail at AWS API call if file existed
