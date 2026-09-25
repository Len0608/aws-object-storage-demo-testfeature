## Test: Test_AwsObjectStorage_UploadFile_NestedPath

**Status**: ✗ Failed

### Output:
```
STDERR:
Local file not found: /home/agent/ue-test-data/test-upload.txt

EXTENSION:
{"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "errors": [{"type": "LocalFileNotFoundError"}]}
```

### Notes:
- The file /home/agent/ue-test-data/test-upload.txt does not exist on the agent host
- Error type: LocalFileNotFoundError (expected given missing test fixture)
- S3 key target was: tests/2024/09/nested-upload.txt
