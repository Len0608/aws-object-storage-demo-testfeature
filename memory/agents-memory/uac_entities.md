# UAC Entities

**Extension:** aws-object-storage-demo-testfeature

---

## Agent Selection

### Available Agents

| Agent Name | Host | IP | Type | Status | Queue | Version |
|------------|------|----|------|--------|-------|---------|
| nginx-with-sidecar - AKS-SIDECAR-TEST | nginx-with-sidecar | 10.244.4.224 | Linux/Unix | Active | AKS-SIDECAR-TEST | 7.9.2.2 |
| sb-agent-ubu - AGNT0012 | sb-agent-ubu | 127.0.1.1 | Linux/Unix | Active | AGNT0012 | 7.9.0.0 |
| UDMG-SB | ip-172-31-2-26.us-east-2.compute.internal | 172.31.2.26 | Linux/Unix | Active | AGNT0118 | 7.9.2.0 |
| pm-agent-ua-98fb75db9-48lt5 - OCP-Agent | pm-agent-ua-98fb75db9-48lt5 | 10.173.1.203 | Linux/Unix | Active | OCP-Agent | 7.9.0.0 |
| workload-identity-ua-0 - UA-DEV-K8S | workload-identity-ua-0 | 10.244.3.98 | Linux/Unix | Active | UA-DEV-K8S | 8.0.0.1 |
| AGT_LINUX_LIBELLE | ip-30-0-2-107.eu-west-1.compute.internal | 30.0.2.107 | Linux/Unix | Active | AGNT0002 | 7.9.2.2 |
| AGT_LINUX_PS1 | packaged-solutions-1 | 30.0.1.111 | Linux/Unix | Active | AGNT0009 | 8.0.0.0 |
| AGT_LINUX_PS5 | ip-30-0-1-83 | 30.0.1.83 | Linux/Unix | Offline | AGNT0071 | 7.7.1.1 |

### Selected Agent

| Field      | Value |
|------------|-------|
| Agent Name | nginx-with-sidecar - AKS-SIDECAR-TEST |
| Host Name  | nginx-with-sidecar |
| IP Address | 10.244.4.224 |
| Type       | Linux/Unix |
| Status     | Active |
| Queue Name | AKS-SIDECAR-TEST |
| Version    | 7.9.2.2 |
| SysID      | 2ed88652f231458ba5d81a4db5ef398c |

**Required OS Type:** Linux/Unix
**Selection rationale:** First active Linux/Unix agent found in the controller agent list; supports the extension's Linux target platform requirement.

---

## Required Entities

### Credentials

| Credential Name | Type | Field Name | Auth Method | Used In Scenarios |
|----------------|------|------------|-------------|-------------------|
| aws-s3-test-creds | Username / Password | aws_credentials | IAM Access Key | Test_AwsObjectStorage_ListObjects_Minimal, Test_AwsObjectStorage_ListObjects_OutputCap, Test_AwsObjectStorage_UploadFile_Minimal, Test_AwsObjectStorage_UploadFile_NestedPath, Test_AwsObjectStorage_UploadFile_Overwrite, Test_AwsObjectStorage_UploadFile_RootKey, Test_AwsObjectStorage_UploadFile_SubFolder, Test_AwsObjectStorage_ListObjects_AfterUpload, Test_AwsObjectStorage_UploadFile_DeepNested, Test_AwsObjectStorage_ListObjects_AfterUpload_WithCap |

**Credential field mapping:**
- **Username field** → AWS Access Key ID (e.g., `AKIAIOSFODNN7EXAMPLE`)
- **Password field** → AWS Secret Access Key (e.g., `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)

> Note: No real AWS credentials were provided. The credential will be created with placeholder values (`test-placeholder-key`). Tests that fail due to invalid credentials are expected and logged as known failures.

### Scripts

*No script fields are defined in this extension's template.*

---

## Created Entities

[Populated by main thread after creation on UAC]

### Credentials

| Credential Name | SysID | Status |
|----------------|-------|--------|
| | | |

### Scripts

*None required.*
