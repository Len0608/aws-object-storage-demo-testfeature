## Issue: Test_AwsObjectStorage_UploadFile_SubFolder

**Status**: ✗ Failed

### Expected:
Upload file to S3 with subfolder path in object key.

### STDOUT:
[empty]

### STDERR:
2026-09-25 10:09:19,816 - extension.py[63] INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 10:09:19,816 - extension.py[70] INFO: Action requested: Upload File
2026-09-25 10:09:19,817 - upload_file.py[45] INFO: Starting upload_file action
ERROR: Local file not found: /home/agent/ue-test-data/test-upload.txt

### Extension Output:
{"exit_code": 1, "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt", "input_fields": {"s3_object_key": "uploads/subdir/test-upload.txt"}, "errors": [{"type": "LocalFileNotFoundError"}]}
