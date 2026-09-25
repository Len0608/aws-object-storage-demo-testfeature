## Issue: Test_AwsObjectStorage_UploadFile_Overwrite

**Status**: ✗ Failed

### Expected:
Upload file to S3, overwriting an existing object at the same key.

### STDOUT:
[empty]

### STDERR:
ERROR: Local file not found: /home/agent/ue-test-data/test-upload.txt

### Extension Output:
{"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "errors": [{"type": "LocalFileNotFoundError"}]}
