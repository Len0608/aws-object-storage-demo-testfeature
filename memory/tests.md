# Test Plan

**Extension:** aws-object-storage-demo-testfeature
**Generated:** 2026-09-25

---

## Test: Test_AwsObjectStorage_ListObjects_Minimal

**Template:** Aws Object Storage Demo Testfeature
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST
**Input Fields:**
- action: List Objects
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-s3-demo
**Expected Results:**
- Task exits with code 0
- output_data.status = "Success: Listed N objects in ue-test-aws-s3-demo"
- output_data.result = "N objects found"
- STDOUT contains a rounded_outline table with columns Key, Size, Last Modified
- Extension Output JSON contains bucket, total_object_count, returned_object_count, truncated, objects

---

## Test: Test_AwsObjectStorage_ListObjects_OutputCap

**Template:** Aws Object Storage Demo Testfeature
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST
**Environment Variables:**
- UE_MAX_OUTPUT_RECORDS: 2
**Input Fields:**
- action: List Objects
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-s3-demo
**Expected Results:**
- Task exits with code 0
- STDOUT table contains at most 2 object rows
- If bucket has more than 2 objects: STDOUT includes NOTE line with total count; STDERR includes WARNING; output_data.result reflects returned_object_count capped at 2
- If bucket has 2 or fewer objects: normal output, no truncation note
- output_data.status = "Success: Listed N objects in ue-test-aws-s3-demo"

---

## Test: Test_AwsObjectStorage_UploadFile_Minimal

**Template:** Aws Object Storage Demo Testfeature
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST
**Input Fields:**
- action: Upload File
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-s3-demo
- local_file: /home/agent/ue-test-data/test-upload.txt
- s3_object_key: tests/test-upload.txt
**Expected Results:**
- Task exits with code 0
- STDOUT contains "Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/tests/test-upload.txt (ETag: ...)"
- output_data.status = "Success: Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/tests/test-upload.txt"
- output_data.result = "ETag: <etag_value>"
- Extension Output JSON contains s3_uri and etag

---

## Test: Test_AwsObjectStorage_UploadFile_NestedPath

**Template:** Aws Object Storage Demo Testfeature
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST
**Input Fields:**
- action: Upload File
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-s3-demo
- local_file: /home/agent/ue-test-data/test-upload.txt
- s3_object_key: tests/2024/09/nested-upload.txt
**Expected Results:**
- Task exits with code 0
- STDOUT contains "Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/tests/2024/09/nested-upload.txt (ETag: ...)"
- output_data.status = "Success: Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/tests/2024/09/nested-upload.txt"
- output_data.result = "ETag: <etag_value>"
- Extension Output JSON contains correct s3_uri with nested path and etag

---

## Test: Test_AwsObjectStorage_UploadFile_Overwrite

**Template:** Aws Object Storage Demo Testfeature
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST
**Input Fields:**
- action: Upload File
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-s3-demo
- local_file: /home/agent/ue-test-data/test-upload.txt
- s3_object_key: tests/test-upload.txt
**Expected Results:**
- Task exits with code 0 (re-run/overwrite is idempotent)
- STDOUT contains "Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/tests/test-upload.txt (ETag: ...)"
- output_data.status = "Success: Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/tests/test-upload.txt"
- output_data.result = "ETag: <etag_value>" (may differ from first upload ETag)
- Extension Output JSON contains s3_uri and etag

---

## Test: Test_AwsObjectStorage_UploadFile_RootKey

**Template:** Aws Object Storage Demo Testfeature
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST
**Input Fields:**
- action: Upload File
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-s3-demo
- local_file: /home/agent/ue-test-data/test-upload.txt
- s3_object_key: root-test-upload.txt
**Expected Results:**
- Task exits with code 0
- STDOUT contains "Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/root-test-upload.txt (ETag: ...)"
- output_data.status = "Success: Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/root-test-upload.txt"
- output_data.result = "ETag: <etag_value>"
- Extension Output JSON contains s3_uri = "s3://ue-test-aws-s3-demo/root-test-upload.txt" and etag

---

## Test: Test_AwsObjectStorage_UploadFile_SubFolder

**Template:** Aws Object Storage Demo Testfeature
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST
**Input Fields:**
- action: Upload File
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-s3-demo
- local_file: /home/agent/ue-test-data/test-upload.txt
- s3_object_key: uploads/subdir/test-upload.txt
**Expected Results:**
- Task exits with code 0
- STDOUT contains "Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/uploads/subdir/test-upload.txt (ETag: ...)"
- output_data.status = "Success: Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/uploads/subdir/test-upload.txt"
- output_data.result = "ETag: <etag_value>"
- Extension Output JSON contains correct s3_uri and etag

---

## Test: Test_AwsObjectStorage_ListObjects_AfterUpload

**Template:** Aws Object Storage Demo Testfeature
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST
**Input Fields:**
- action: List Objects
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-s3-demo
**Expected Results:**
- Task exits with code 0
- STDOUT table lists objects including tests/test-upload.txt uploaded in prior test
- output_data.status = "Success: Listed N objects in ue-test-aws-s3-demo" where N >= 1
- output_data.result = "N objects found"
- Extension Output JSON total_object_count >= 1

---

## Test: Test_AwsObjectStorage_UploadFile_DeepNested

**Template:** Aws Object Storage Demo Testfeature
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST
**Input Fields:**
- action: Upload File
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-s3-demo
- local_file: /home/agent/ue-test-data/test-upload.txt
- s3_object_key: tests/a/b/c/d/deep-nested.txt
**Expected Results:**
- Task exits with code 0
- STDOUT contains "Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/tests/a/b/c/d/deep-nested.txt (ETag: ...)"
- output_data.status = "Success: Uploaded test-upload.txt to s3://ue-test-aws-s3-demo/tests/a/b/c/d/deep-nested.txt"
- output_data.result = "ETag: <etag_value>"
- Extension Output JSON contains correct deeply nested s3_uri and etag

---

## Test: Test_AwsObjectStorage_ListObjects_AfterUpload_WithCap

**Template:** Aws Object Storage Demo Testfeature
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST
**Environment Variables:**
- UE_MAX_OUTPUT_RECORDS: 3
**Input Fields:**
- action: List Objects
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-s3-demo
**Expected Results:**
- Task exits with code 0
- STDOUT table contains at most 3 object rows
- If bucket has more than 3 objects: NOTE and WARNING lines appear; truncated=true in JSON
- output_data.status = "Success: Listed N objects in ue-test-aws-s3-demo"
- Extension Output JSON returned_object_count <= 3 and total_object_count >= 1

---
