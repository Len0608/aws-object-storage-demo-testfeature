# Universal Extension Requirements (Refined)

**Extension Name:** AWS Object Storage
**Original Generated:** Not specified
**Refined:** 2026-09-25
**Agent_id:** Not specified
**Requirements Completeness:** Moderate Detail
**Target Platform:** Linux (x86_64)

---

# Table of Contents

1. [Overview](#overview)
2. [Actions](#actions)
   - 2.1 [Action 1 — List Objects](#action-1--list-objects)
   - 2.2 [Action 2 — Upload File](#action-2--upload-file)
3. [Input Requirements](#input-requirements)
   - 3.1 [Connection Parameters](#connection-parameters)
   - 3.2 [List Objects — Action-Specific Fields](#list-objects--action-specific-fields)
   - 3.3 [Upload File — Action-Specific Fields](#upload-file--action-specific-fields)
4. [Output Requirements](#output-requirements)
   - 4.1 [On Success](#on-success)
   - 4.2 [On Error](#on-error)
5. [Authentication Requirements](#authentication-requirements)
6. [Environment Variables](#environment-variables)
7. [Operational Behavior](#operational-behavior)
8. [Implementation Notes](#implementation-notes)
   - 8.1 [Python Compatibility](#python-compatibility)
   - 8.2 [Target Platform](#target-platform)
   - 8.3 [Third-Party Services and Tools](#third-party-services-and-tools)
   - 8.4 [Error Handling](#error-handling)
   - 8.5 [Resource Cleanup](#resource-cleanup)
9. [Requirements Summary](#requirements-summary)
10. [Document Change History](#document-change-history)
11. [References](#references)

---

# Overview

This document defines the functional requirements for the **AWS Object Storage** Universal Extension for Stonebranch Universal Automation Center (UAC).

**Integration Purpose:** The extension provides a minimal AWS S3 integration demonstrating that S3 operations can be implemented and executed within UAC. It exposes two actions — listing objects in a bucket and uploading a local file to a bucket — using the `boto3` SDK bundled with the extension. The primary purpose is demonstration/MVP; simplicity takes priority over advanced features.

---

# Actions

## Action 1 — List Objects

**Functional Requirements:**

1. The extension must connect to AWS S3 using the provided credentials and region.
2. The extension must retrieve the list of objects in the specified S3 bucket.
3. The extension must display object metadata per object: Object Key, Size (human-readable, e.g., "1.2 MB"), and Last Modified timestamp.
4. The STDOUT output must be formatted as a `rounded_outline` ASCII table with columns: **Key | Size | Last Modified**.
5. The extension must apply a configurable cap on the number of objects returned, controlled by the `UE_MAX_OUTPUT_RECORDS` environment variable (default: 100 objects).
6. If the number of objects in the bucket exceeds the cap, the extension must:
   - Display a truncation note at the bottom of the STDOUT table.
   - Emit a warning to STDERR showing the total object count in the bucket and the applied limit.
   - Include the truncated object list plus the total object count as metadata in the Extension Output JSON.
7. The Extension Output JSON must contain the (possibly truncated) list of objects and the total object count in the bucket.
8. The **Status** output field must be populated with a short action summary (e.g., `"Success: Listed 42 objects in my-bucket"`).
9. The **Result** output field must be populated with the object count (e.g., `"42 objects found"`).

---

## Action 2 — Upload File

**Functional Requirements:**

1. The extension must connect to AWS S3 using the provided credentials and region.
2. The extension must upload the specified local file from the UAC agent host to the specified S3 bucket and S3 object key.
3. The extension must read the local file path and the target S3 object key from the task input fields.
4. On successful upload, the extension must capture the ETag returned by the S3 API.
5. The **Status** output field must be populated with a short action summary (e.g., `"Success: Uploaded report.csv to s3://my-bucket/reports/report.csv"`).
6. The **Result** output field must be populated with the ETag of the uploaded object (e.g., `ETag: "d41d8cd98f00b204e9800998ecf8427e"`).
7. The Extension Output JSON must contain the S3 URI of the uploaded object and the ETag.

---

# Input Requirements

## Connection Parameters

These fields apply to both actions.

- **AWS Credentials** (Credential, required): AWS IAM credential used to authenticate with the S3 API. The credential must supply an access key ID (user) and a secret access key (password).
  - Applicability: List Objects, Upload File

- **AWS Region** (Plain Text, required): The AWS region where the target S3 bucket resides.
  - Example: `us-east-1`
  - Applicability: List Objects, Upload File

- **Bucket Name** (Plain Text, required): The name of the S3 bucket to operate on.
  - Example: `my-demo-bucket`
  - Applicability: List Objects, Upload File

- **Action** (Choice, required): Selects which operation to perform.
  - Options: `List Objects`, `Upload File`
  - Default: `List Objects`
  - Applicability: All — controls which action-specific fields are shown

---

## List Objects — Action-Specific Fields

No additional action-specific input fields are required for the List Objects action. All required inputs are covered by the connection parameters.

---

## Upload File — Action-Specific Fields

These fields are shown only when **Action** is set to `Upload File`.

- **Local File** (Plain Text, required when Action = Upload File): The absolute path on the UAC agent host to the local file that must be uploaded.
  - Example: `/home/agent/data/report.csv`
  - Applicability: Upload File only

- **S3 Object Key** (Plain Text, required when Action = Upload File): The target object key (path) within the S3 bucket where the file will be stored.
  - Example: `reports/report.csv`
  - Applicability: Upload File only

---

# Output Requirements

## On Success

**Output-Only UI Fields (both actions):**

| Field Name | Type | Description |
|---|---|---|
| Status | Plain Text | Short action summary visible in the UAC task list view |
| Result | Plain Text | Action-specific supporting detail |

**List Objects — Success:**

- Return code: `0`
- Status description: `"Success: Listed <N> objects in <bucket-name>"`
- Result field: `"<N> objects found"`
- STDOUT output: `rounded_outline` ASCII table with columns **Key | Size | Last Modified**, one row per object (up to the cap limit). If truncated, a note is appended below the table.
- STDERR output: If the output is truncated, a warning line is written to STDERR showing the total object count and the applied cap (e.g., `"WARNING: Bucket contains 350 objects; output capped at 100 by UE_MAX_OUTPUT_RECORDS"`).
- Extension Output (JSON):
  ```json
  {
    "bucket": "<bucket-name>",
    "total_object_count": 350,
    "returned_object_count": 100,
    "truncated": true,
    "objects": [
      {"key": "reports/report.csv", "size": "1.2 MB", "last_modified": "2026-09-24T10:00:00Z"},
      ...
    ]
  }
  ```

**Upload File — Success:**

- Return code: `0`
- Status description: `"Success: Uploaded <filename> to s3://<bucket-name>/<s3-object-key>"`
- Result field: `ETag: "<etag-value>"`
- STDOUT output: Confirmation message with the S3 URI and ETag.
- Extension Output (JSON):
  ```json
  {
    "s3_uri": "s3://<bucket-name>/<s3-object-key>",
    "etag": "<etag-value>"
  }
  ```

**Success Criteria:**

1. The AWS API call completes without error.
2. For List Objects: at least zero objects are returned (an empty bucket is a valid success).
3. For Upload File: the S3 API returns an ETag confirming the object was stored.
4. Return code is `0`.
5. Status and Result output fields are populated.

---

## On Error

**Failure Scenarios:**

| Scenario | Description | Root Causes | Return Code | Status Description Pattern |
|---|---|---|---|---|
| Authentication Failure | AWS rejects the provided credentials | Invalid access key ID or secret access key | Non-zero | `"Error: Authentication failed — <AWS error message>"` |
| Authorization Failure | Credentials are valid but lack S3 permissions | IAM policy does not allow the required S3 action on the bucket | Non-zero | `"Error: Access denied — <AWS error message>"` |
| Bucket Not Found | The specified bucket does not exist or is not accessible | Incorrect bucket name, wrong region, or bucket deleted | Non-zero | `"Error: Bucket not found — <bucket-name>"` |
| Local File Not Found | The local file path does not exist on the agent host | Incorrect path or file deleted before upload | Non-zero | `"Error: Local file not found — <local-file-path>"` |
| Network / Connectivity Error | Cannot reach the AWS S3 endpoint | Network outage, DNS failure, proxy misconfiguration | Non-zero | `"Error: Connection failed — <AWS error message>"` |
| S3 API Error | Unexpected error returned by the AWS S3 API | Service-side error, throttling, or unsupported operation | Non-zero | `"Error: S3 API error — <AWS error code>: <AWS error message>"` |

**Input Validation:**

- All required fields must be non-empty; if any required field is missing, the extension must fail with a clear error message before making any API call.

---

# Authentication Requirements

The extension must authenticate to AWS S3 using IAM access key credentials. The credential is supplied via a UAC Credential field. The access key ID is read from the credential's `user` attribute and the secret access key from the `password` attribute. No other authentication method (IAM role, SSO, STS) is required for this MVP.

---

# Environment Variables

- **`UE_MAX_OUTPUT_RECORDS`** (integer, optional): Maximum number of S3 objects returned in STDOUT and Extension Output for the List Objects action. If not set, the default value is `100`. Can be set per task in the UAC task definition's environment variables without requiring a code change.

---

# Operational Behavior

**Dynamic Choice Fields:**
Not applicable. No dynamic dropdown population is required.

**Cancel Action:**
Standard UAC cancel behavior applies. No custom cancel logic is required.

**Re-run Capability:**
Both actions are idempotent from an infrastructure perspective. Re-running List Objects always fetches the current bucket state. Re-running Upload File overwrites the object at the specified S3 key if it already exists. No special re-run handling is required.

**Progress Reporting:**
No progress bar or incremental progress reporting is required. A single success or failure message is sufficient for this MVP.

**Dynamic Commands:**
Not applicable. No dynamic commands are required.

---

# Implementation Notes

## Python Compatibility

Not specified specifically. Targeting compatibility for Python 3.11.

## Target Platform

Linux (x86_64). C-extension modules with a confirmed `manylinux_2_17_x86_64` wheel are viable in addition to pure-Python modules. All selected modules for this extension are pure-Python, so this constraint is satisfied trivially.

## Third-Party Services and Tools

**AWS S3 (Amazon Simple Storage Service)**
- Short Description: Cloud object storage service used to list and upload objects.
- Version constraints: No minimum API version constraint; standard `list_objects_v2` and `put_object` operations are used.
- Integration approach: HTTP-based interaction via the `boto3` SDK.

**boto3**
- Short Description: Official AWS SDK for Python; provides the S3 client.
- Version: `1.43.102`
- Type: Pure Python

**botocore**
- Short Description: Core AWS library (boto3 dependency); handles HTTP request signing and AWS authentication.
- Version: `1.43.102`
- Type: Pure Python

**s3transfer**
- Short Description: boto3 dependency; manages efficient S3 transfers.
- Version: `0.19.2`
- Type: Pure Python

**jmespath**
- Short Description: boto3 dependency; JSON query language used internally by boto3.
- Version: `1.1.0`
- Type: Pure Python

**python-dateutil**
- Short Description: boto3 dependency; parses ISO 8601 date/time values from S3 metadata.
- Version: `2.9.0`
- Type: Pure Python

**tabulate**
- Short Description: Formats the List Objects result as a `rounded_outline` ASCII table for STDOUT.
- Version: `0.10.0`
- Type: Pure Python

All modules must be bundled with the extension. Nothing must be installed separately on the UAC agent.

## Error Handling

- **Error categories:** Authentication/authorization errors, bucket-not-found errors, local file errors, network/connectivity errors, and general S3 API errors.
- **Error handling strategy:** All AWS API exceptions must be caught, a descriptive error message must be written, and a non-zero return code must be set. The extension must not raise unhandled exceptions.
- **Recovery mechanisms:** None required for this MVP. No automatic retry logic is needed.

## Resource Cleanup

- **Cleanup scenarios:** File handles opened for upload must be closed after the operation completes, whether it succeeds or fails.
- **Strategy:** Use standard Python context managers (`with` statement) to ensure file handles are released automatically.

---

# Requirements Summary

The **AWS Object Storage** Universal Extension is an MVP/demo integration that exposes two S3 operations within UAC:

1. **List Objects** — retrieves and displays objects in an S3 bucket as a formatted ASCII table (Key, human-readable Size, Last Modified), capped at `UE_MAX_OUTPUT_RECORDS` (default 100) to prevent large outputs.
2. **Upload File** — uploads a local file from the UAC agent host to a specified S3 bucket and object key, returning the ETag on success.

Both actions use IAM access key credentials and require AWS Region and Bucket Name as shared inputs. Upload File additionally requires Local File path and S3 Object Key. Results are surfaced in two UAC output fields (Status and Result) and as structured Extension Output JSON. All `boto3` dependencies plus `tabulate` must be bundled with the extension. The target platform is Linux (x86_64).

---

# Document Change History

- **2026-09-25**: Initial requirements captured — Moderate Detail. Core intent, two actions, primary input fields, and Python library specified.
- **2026-09-25**: Comprehensive refinement based on 4 clarification questions and user feedback. Output design finalized: tabulate formatting confirmed (Q1), List Objects columns defined as Key/Size/Last Modified (Q2), `UE_MAX_OUTPUT_RECORDS` cap with default 100 adopted (Q3), two UAC output fields (Status + Result) confirmed (Q4).

---

# References

- Original Requirements Document: `memory/requirements.md`
- Original Requirements Q&A Document: `memory/agents-memory/requirements-QnA.md`
