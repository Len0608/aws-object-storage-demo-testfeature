# Test Issues — aws-object-storage-demo-testfeature

**Run Date:** 2026-09-25
**Controller:** https://ps1.stonebranchdev.cloud
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST

---

## Upload File Tasks (6 tasks) — LocalFileNotFoundError

All upload tasks failed because the test fixture file `/home/agent/ue-test-data/test-upload.txt` does not exist on the agent host.

**Affected tasks:**
- Test_AwsObjectStorage_UploadFile_Minimal
- Test_AwsObjectStorage_UploadFile_DeepNested
- Test_AwsObjectStorage_UploadFile_NestedPath
- Test_AwsObjectStorage_UploadFile_Overwrite
- Test_AwsObjectStorage_UploadFile_RootKey
- Test_AwsObjectStorage_UploadFile_SubFolder

**Error type:** `LocalFileNotFoundError`
**Error message:** `Local file not found: /home/agent/ue-test-data/test-upload.txt`

**Root cause:** The extension correctly validates local file existence before attempting S3 upload. The test fixture file was not pre-staged on the agent.

---

## List Objects Tasks (4 tasks) — InvalidAccessKeyId

All list tasks failed because the `aws-s3-test-creds` credential contains placeholder values (`test-placeholder-key`) that are not valid AWS credentials.

**Affected tasks:**
- Test_AwsObjectStorage_ListObjects_Minimal
- Test_AwsObjectStorage_ListObjects_AfterUpload
- Test_AwsObjectStorage_ListObjects_OutputCap
- Test_AwsObjectStorage_ListObjects_AfterUpload_WithCap

**Error type:** `S3ApiError`
**Error message:** `S3 API error: InvalidAccessKeyId: The AWS Access Key Id you provided does not exist in our records.`

**Root cause:** The extension successfully resolved the credential and reached the AWS S3 API, but the placeholder access key ID was rejected by AWS.

---

## Summary

| Root Cause | Tasks Affected | Known Failure |
|---|---|---|
| Test fixture file missing on agent | 6 | Yes |
| Placeholder AWS credentials | 4 | Yes |
