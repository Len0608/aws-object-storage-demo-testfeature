## Issue: Test_AwsObjectStorage_UploadFile_NestedPath

**Status**: ✗ Failed

### Expected:
Upload file to S3 with nested path in object key.

### STDOUT:
[empty]

### STDERR:
2026-09-25 10:09:44,840 - extension.py[63] INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 10:09:44,840 - extension.py[70] INFO: Action requested: Upload File
ERROR: Local file not found: /home/agent/ue-test-data/test-upload.txt

### Extension Output:
{"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "errors": [{"type": "LocalFileNotFoundError"}]}
