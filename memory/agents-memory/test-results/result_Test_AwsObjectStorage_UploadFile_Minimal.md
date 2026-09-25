## Test: Test_AwsObjectStorage_UploadFile_Minimal

**Status**: ✗ Failed

### Output:
```
STDERR:
2026-09-25 10:16:41,289 - extension.py[63] INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 10:16:41,289 - upload_file.py[85] ERROR: Local file not found: /home/agent/ue-test-data/test-upload.txt
2026-09-25 10:16:41,290 - extension.py[90] ERROR: Execution error: Local file not found: /home/agent/ue-test-data/test-upload.txt

EXTENSION:
{"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "errors": [{"type": "LocalFileNotFoundError"}]}
```

### Notes:
- The file /home/agent/ue-test-data/test-upload.txt does not exist on the agent host
- Error type: LocalFileNotFoundError (expected given missing test fixture)
