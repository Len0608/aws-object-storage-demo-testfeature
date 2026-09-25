## Issue: Test_AwsObjectStorage_UploadFile_Minimal

**Status**: ✗ Failed

### Expected:
File uploaded successfully to S3 bucket "ue-test-aws-s3-demo" at key "tests/test-upload.txt"

### STDOUT:
[empty]

### STDERR:
2026-09-25 10:16:41,289 - 139644981192256 AsyEvent[EXTENSION_START] - extension.py[63] INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 10:16:41,289 - 139644981192256 AsyEvent[EXTENSION_START] - extension.py[70] INFO: Action requested: Upload File
2026-09-25 10:16:41,289 - 139644981192256 AsyEvent[EXTENSION_START] - extension.py[76] INFO: Executing action: Upload File
2026-09-25 10:16:41,289 - 139644981192256 AsyEvent[EXTENSION_START] - upload_file.py[45] INFO: Starting upload_file action
2026-09-25 10:16:41,289 - 139644981192256 AsyEvent[EXTENSION_START] - upload_file.py[78] INFO: Input validation passed
2026-09-25 10:16:41,289 - 139644981192256 AsyEvent[EXTENSION_START] - upload_file.py[83] INFO: Checking local file existence: /home/agent/ue-test-data/test-upload.txt
2026-09-25 10:16:41,289 - 139644981192256 AsyEvent[EXTENSION_START] - upload_file.py[85] ERROR: Local file not found: /home/agent/ue-test-data/test-upload.txt
2026-09-25 10:16:41,290 - 139644981192256 AsyEvent[EXTENSION_START] - extension.py[90] ERROR: Execution error: Local file not found: /home/agent/ue-test-data/test-upload.txt
2026-09-25 10:16:41,333 - 139644981192256 AsyEvent[EXTENSION_START] - extension_start_result.py[221] ERROR: Error in extension: /var/opt/universal/uag/extensions/.aws-object-storage-demo-testfeature/extension.py:187 - Local file not found: /home/agent/ue-test-data/test-upload.txt

### Extension Output:
{
  "exit_code": 1,
  "status_description": "Local file not found: /home/agent/ue-test-data/test-upload.txt",
  "metadata": {
    "version": "1.0.0",
    "extension": "aws-object-storage-demo-testfeature"
  },
  "input_fields": {
    "action": ["Upload File"],
    "aws_credentials": {"user": "test-placeholder-key", "password": "****", "token": "", "passphrase": ""},
    "aws_region": "us-east-1",
    "bucket_name": "ue-test-aws-s3-demo",
    "local_file": "/home/agent/ue-test-data/test-upload.txt",
    "s3_object_key": "tests/test-upload.txt"
  },
  "result": {},
  "errors": [
    {
      "type": "LocalFileNotFoundError",
      "message": "Local file not found: /home/agent/ue-test-data/test-upload.txt",
      "exit_code": 1
    }
  ]
}
