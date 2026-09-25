## Issue: Test_AwsObjectStorage_UploadFile_RootKey

**Status**: ✗ Failed

### Expected:
File uploaded successfully to S3 bucket "ue-test-aws-s3-demo" at key "root-test-upload.txt"

### STDOUT:
[empty]

### STDERR:
2026-09-25 10:1x:xx - upload_file.py ERROR: Local file not found: /home/agent/ue-test-data/test-upload.txt
2026-09-25 10:1x:xx - extension.py ERROR: Execution error: Local file not found: /home/agent/ue-test-data/test-upload.txt

### Extension Output:
{"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "errors": [{"type": "LocalFileNotFoundError", "message": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "exit_code": 1}]}
