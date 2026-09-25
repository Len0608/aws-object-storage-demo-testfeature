## Issue: Test_AwsObjectStorage_UploadFile_Overwrite

**Status**: ✗ Failed

### Expected:
Upload file to same S3 key to test overwrite behaviour.

### STDOUT:
[empty]

### STDERR:
Local file not found: /home/agent/ue-test-data/test-upload.txt

### Extension Output:
{"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt"}

### Notes:
- Local test file /home/agent/ue-test-data/test-upload.txt does not exist on agent host.
