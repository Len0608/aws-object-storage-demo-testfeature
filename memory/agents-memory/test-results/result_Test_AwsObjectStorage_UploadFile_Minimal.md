## Test: Test_AwsObjectStorage_UploadFile_Minimal

**Status**: ✗ Failed

### Output:
```
STDERR:
2026-09-25 09:59:56,977 - upload_file.py ERROR: Local file not found: /home/agent/ue-test-data/test-upload.txt

EXTENSION:
{"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "errors": [{"type": "LocalFileNotFoundError"}]}
```

### Notes:
- Local test file /home/agent/ue-test-data/test-upload.txt does not exist on agent host.
- Extension ran correctly, dispatched to Upload File action, validated inputs, and detected missing file.
