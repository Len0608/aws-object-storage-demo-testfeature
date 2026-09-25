## Issue: Test_AwsObjectStorage_ListObjects_Minimal

**Status**: ✗ Failed

### Expected:
List objects in S3 bucket successfully (minimal configuration).

### STDOUT:
[empty]

### STDERR:
2026-09-25 10:06:19,806 - 140419551700544 AsyEvent[EXTENSION_START] - extension.py[63] INFO: aws-object-storage-demo-testfeature v1.0.0 started
2026-09-25 10:06:19,806 - 140419551700544 AsyEvent[EXTENSION_START] - extension.py[70] INFO: Action requested: List Objects
2026-09-25 10:06:19,807 - 140419551700544 AsyEvent[EXTENSION_START] - extension.py[76] INFO: Executing action: List Objects
2026-09-25 10:06:19,807 - 140419551700544 AsyEvent[EXTENSION_START] - list_objects.py[53] INFO: Starting list_objects action
2026-09-25 10:06:19,807 - 140419551700544 AsyEvent[EXTENSION_START] - list_objects.py[78] INFO: Input validation passed
2026-09-25 10:06:19,807 - 140419551700544 AsyEvent[EXTENSION_START] - list_objects.py[102] INFO: Initialising S3 client for region: us-east-1
2026-09-25 10:06:19,807 - 140419551700544 AsyEvent[EXTENSION_START] - utility.py[80] INFO: Initialising S3 client for region: us-east-1
2026-09-25 10:06:19,932 - 140419551700544 AsyEvent[EXTENSION_START] - list_objects.py[112] INFO: Retrieving objects from bucket: ue-test-aws-s3-demo
2026-09-25 10:06:19,932 - 140419551700544 AsyEvent[EXTENSION_START] - utility.py[113] INFO: Listing objects in bucket: ue-test-aws-s3-demo
2026-09-25 10:06:20,296 - 140419551700544 AsyEvent[EXTENSION_START] - utility.py[229] ERROR: S3 ClientError — code: InvalidAccessKeyId, message: The AWS Access Key Id you provided does not exist in our records.
2026-09-25 10:06:20,296 - 140419551700544 AsyEvent[EXTENSION_START] - extension.py[90] ERROR: Execution error: S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.
2026-09-25 10:06:20,363 - 140419551700544 AsyEvent[EXTENSION_START] - extension_start_result.py[221] ERROR: Error in extension: /var/opt/universal/uag/extensions/.aws-object-storage-demo-testfeature/extension.py:187 - S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{
  "exit_code": 1,
  "status_description": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.",
  "metadata": {
    "version": "1.0.0",
    "extension": "aws-object-storage-demo-testfeature"
  },
  "input_fields": {
    "action": ["List Objects"],
    "aws_credentials": {"user": "test-placeholder-key", "password": "****", "token": "", "passphrase": ""},
    "aws_region": "us-east-1",
    "bucket_name": "ue-test-aws-s3-demo",
    "local_file": "",
    "s3_object_key": ""
  },
  "result": {},
  "errors": [
    {
      "type": "S3ApiError",
      "message": "S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.",
      "exit_code": 1
    }
  ]
}
