## Issue: Test_AwsObjectStorage_UploadFile_Minimal

**Status**: ✗ Failed

### Expected:
Upload a local file to S3 bucket (minimal configuration).

### STDOUT:
[empty]

### STDERR:
2026-09-25 10:08:53,705 - extension.py[63] INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 10:08:53,705 - extension.py[70] INFO: Action requested: Upload File
2026-09-25 10:08:53,705 - upload_file.py[78] INFO: Input validation passed
2026-09-25 10:08:53,705 - upload_file.py[83] INFO: Checking local file existence: /home/agent/ue-test-data/test-upload.txt
ERROR: Local file not found: /home/agent/ue-test-data/test-upload.txt

### Extension Output:
{"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "errors": [{"type": "LocalFileNotFoundError", "message": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "exit_code": 1}]}
