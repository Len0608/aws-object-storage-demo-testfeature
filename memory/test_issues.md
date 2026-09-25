# Test Issues Log

**Run Date:** 2026-09-25  
**Extension:** aws-object-storage-demo-testfeature v1.0.0  
**Controller:** https://ps1.stonebranchdev.cloud  
**Agent:** nginx-with-sidecar - AKS-SIDECAR-TEST

---

## Summary

All 10 tests failed. Two distinct failure categories observed:

### Category A: Invalid AWS Credentials (4 tests — List Objects)
Placeholder credential `test-placeholder-key` was rejected by AWS with `InvalidAccessKeyId`.  
The extension reached the AWS API call successfully — input validation, dispatch, and S3 client init all worked correctly.

### Category B: Missing Local File (6 tests — Upload File)
Test file `/home/agent/ue-test-data/test-upload.txt` does not exist on the agent host.  
The extension loaded, dispatched, and validated inputs correctly before reporting `LocalFileNotFoundError`.

---

## Failed Tasks

### Test_AwsObjectStorage_ListObjects_Minimal
- **Status**: ✗ Failed
- **Error**: `S3ApiError: InvalidAccessKeyId`
- **Root Cause**: Placeholder credential

### Test_AwsObjectStorage_ListObjects_OutputCap
- **Status**: ✗ Failed
- **Error**: `S3ApiError: InvalidAccessKeyId`
- **Root Cause**: Placeholder credential

### Test_AwsObjectStorage_ListObjects_AfterUpload
- **Status**: ✗ Failed
- **Error**: `S3ApiError: InvalidAccessKeyId`
- **Root Cause**: Placeholder credential

### Test_AwsObjectStorage_ListObjects_AfterUpload_WithCap
- **Status**: ✗ Failed
- **Error**: `S3ApiError: InvalidAccessKeyId`
- **Root Cause**: Placeholder credential

### Test_AwsObjectStorage_UploadFile_Minimal
- **Status**: ✗ Failed
- **Error**: `LocalFileNotFoundError: /home/agent/ue-test-data/test-upload.txt`
- **Root Cause**: Test file absent on agent host

### Test_AwsObjectStorage_UploadFile_SubFolder
- **Status**: ✗ Failed
- **Error**: `LocalFileNotFoundError: /home/agent/ue-test-data/test-upload.txt`
- **Root Cause**: Test file absent on agent host

### Test_AwsObjectStorage_UploadFile_NestedPath
- **Status**: ✗ Failed
- **Error**: `LocalFileNotFoundError: /home/agent/ue-test-data/test-upload.txt`
- **Root Cause**: Test file absent on agent host

### Test_AwsObjectStorage_UploadFile_DeepNested
- **Status**: ✗ Failed
- **Error**: `LocalFileNotFoundError: /home/agent/ue-test-data/test-upload.txt`
- **Root Cause**: Test file absent on agent host

### Test_AwsObjectStorage_UploadFile_RootKey
- **Status**: ✗ Failed
- **Error**: `LocalFileNotFoundError: /home/agent/ue-test-data/test-upload.txt`
- **Root Cause**: Test file absent on agent host

### Test_AwsObjectStorage_UploadFile_Overwrite
- **Status**: ✗ Failed
- **Error**: `LocalFileNotFoundError: /home/agent/ue-test-data/test-upload.txt`
- **Root Cause**: Test file absent on agent host
