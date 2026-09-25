# Test Issues Summary

**Run Date:** 2026-09-25  
**Extension:** aws-object-storage-demo-testfeature v1.0.0  
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST  
**Template:** Aws Object Storage Demo Testfeature

---

## Failure Category 1: Invalid AWS Credentials (4 tasks)

Affects all **List Objects** tests. Root cause: placeholder credential `aws-s3-test-creds` uses `test-placeholder-key` which is rejected by AWS.

**Error:** `S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.`

Tasks affected:
- Test_AwsObjectStorage_ListObjects_Minimal
- Test_AwsObjectStorage_ListObjects_AfterUpload
- Test_AwsObjectStorage_ListObjects_AfterUpload_WithCap
- Test_AwsObjectStorage_ListObjects_OutputCap

**Positive observations:**
- Extension starts successfully.
- Action is dispatched correctly.
- Input validation passes.
- S3 client initialises and reaches AWS API before failing on auth.
- Error is caught and returned as structured JSON with exit code 1.

---

## Failure Category 2: Missing Local File (6 tasks)

Affects all **Upload File** tests. Root cause: local test file `/home/agent/ue-test-data/test-upload.txt` does not exist on the agent host.

**Error:** `Local file not found: /home/agent/ue-test-data/test-upload.txt`

Tasks affected:
- Test_AwsObjectStorage_UploadFile_Minimal
- Test_AwsObjectStorage_UploadFile_DeepNested
- Test_AwsObjectStorage_UploadFile_NestedPath
- Test_AwsObjectStorage_UploadFile_Overwrite
- Test_AwsObjectStorage_UploadFile_RootKey
- Test_AwsObjectStorage_UploadFile_SubFolder

**Positive observations:**
- Extension starts successfully.
- Action is dispatched correctly.
- Input validation passes.
- Extension correctly checks for local file existence before attempting upload.
- Error is caught and returned as structured JSON with exit code 1.

---

## JSON Fix Applied During Test Run

All 10 task JSON files were missing the required `type` field. The field was added with value `taskUniversal` before tasks could be created on UAC. Five tasks also required deletion and recreation because they were linked to an older template (`Ue 3 Aws Object Storage`) instead of the current template (`Aws Object Storage Demo Testfeature`).
