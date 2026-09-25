# AWS Object Storage - Implementation Analysis

**Extension Name:** *AWS Object Storage (aws-object-storage-demo-testfeature)*
**Universal Template Name:** *Aws Object Storage Demo Testfeature*
**Target Platform:** Linux (x86_64)

---

## Extension Overview

This extension provides an MVP/demo AWS S3 integration for Stonebranch UAC. It exposes two actions — listing objects in an S3 bucket and uploading a local file to an S3 bucket — using the bundled `boto3` SDK. Authentication uses IAM access key credentials supplied via a UAC Credential field. Simplicity takes priority over advanced features.

---

# Template Fields

## 1. Input Fields

**action**
- **Type**: Choice Field (Single-select)
- **Visible When**: always
- **Required When**: always
- **Options**:
  - `List Objects` — Retrieves and displays all objects in the specified S3 bucket
  - `Upload File` — Uploads a local file from the agent host to the specified S3 bucket
- **Default Value**: `List Objects`
- **Validation**:
  - Must be one of the defined options
- **Purpose**: Selects which S3 operation to perform; controls visibility of action-specific fields

---

**aws_credentials**
- **Type**: Credential Field
- **Visible When**: always
- **Required When**: always
- **Validation**:
  - Must reference a valid UAC Credential record
  - The `user` attribute holds the AWS Access Key ID
  - The `password` attribute holds the AWS Secret Access Key
- **Purpose**: Supplies the IAM access key credentials used to authenticate all S3 API calls. Access Key ID is read from `credential.user`; Secret Access Key is read from `credential.password`

---

**aws_region**
- **Type**: Text Field
- **Visible When**: always
- **Required When**: always
- **Validation**:
  - Must be a non-empty string
  - Must be a valid AWS region identifier format (e.g., lowercase letters, digits, hyphens)
- **Purpose**: The AWS region where the target S3 bucket resides; passed directly to the boto3 S3 client
- **Example**: `us-east-1`

---

**bucket_name**
- **Type**: Text Field
- **Visible When**: always
- **Required When**: always
- **Validation**:
  - Must be a non-empty string
- **Purpose**: The name of the S3 bucket to operate on; used in all S3 API calls
- **Example**: `my-demo-bucket`

---

**local_file**
- **Type**: Text Field
- **Visible When**: action "value is equal to" `Upload File`. It is required when it's visible
- **Required When**: action "value is equal to" `Upload File`
- **Validation**:
  - Must be a non-empty string
  - Must be an absolute path
- **Purpose**: The absolute filesystem path on the UAC agent host of the local file to upload; validated for existence before the S3 API call is made
- **Example**: `/home/agent/data/report.csv`

---

**s3_object_key**
- **Type**: Text Field
- **Visible When**: action "value is equal to" `Upload File`. It is required when it's visible
- **Required When**: action "value is equal to" `Upload File`
- **Validation**:
  - Must be a non-empty string
- **Purpose**: The target S3 object key (path within the bucket) where the uploaded file will be stored
- **Example**: `reports/report.csv`

---

## 2. Output Fields

**status**
- **Type**: Text Output
- **Purpose**: Short action summary displayed in the UAC task list view; populated by the extension on success or failure
- **Examples**:
  - `"Success: Listed 42 objects in my-demo-bucket"`
  - `"Success: Uploaded report.csv to s3://my-demo-bucket/reports/report.csv"`
  - `"Error: Authentication failed — InvalidClientTokenId"`
  - `"Error: Bucket not found — my-demo-bucket"`
  - `"Error: Local file not found — /home/agent/data/report.csv"`

---

**result**
- **Type**: Text Output
- **Purpose**: Action-specific supporting detail; populated on success to provide the most operationally useful output value
- **Examples**:
  - `"42 objects found"` (List Objects success)
  - `ETag: "d41d8cd98f00b204e9800998ecf8427e"` (Upload File success)

---

## 3. Field Ordering

The task form uses a **2-column grid layout**.

**Field Order (Visual Layout):**

```
┌─────────────────────────────────────────┐
│                 action                  │  ← Full-width
├─────────────────────────────────────────┤
│            aws_credentials              │  ← Full-width (credential)
├───────────────────┬─────────────────────┤
│    aws_region     │    bucket_name      │  ← Half-width pair
├─────────────────────────────────────────┤
│              local_file                 │  ← Full-width (Upload File only)
├─────────────────────────────────────────┤
│            s3_object_key                │  ← Full-width (Upload File only)
├─────────────────────────────────────────┤
│                 status                  │  ← Full-width (Output Only)
├─────────────────────────────────────────┤
│                 result                  │  ← Full-width (Output Only)
└─────────────────────────────────────────┘
```

---

# Actions

## Action 1: List Objects

**Description**: Connects to AWS S3 using the provided credentials and region, retrieves the complete list of objects from the specified bucket, and displays object metadata (Key, human-readable Size, Last Modified) as a `rounded_outline` ASCII table on STDOUT. Output is capped by the `UE_MAX_OUTPUT_RECORDS` environment variable (default: 100). If truncated, a note is appended to STDOUT and a warning is written to STDERR. Both the truncated object list and the total object count are returned in the Extension Output JSON.

### Input Requirements

- **action** — must be `List Objects`
- **aws_credentials** — IAM access key ID (`credential.user`) and secret access key (`credential.password`)
- **aws_region** — target AWS region
- **bucket_name** — name of the S3 bucket to list

### Execution Flow

**Step 1: Input Validation**
- Verify aws_credentials is provided and both `user` (Access Key ID) and `password` (Secret Access Key) are non-empty. If invalid, raise `ValidationError` with exit code 20 and a descriptive message before making any API call.
- Verify aws_region and bucket_name are non-empty strings. If either is missing, raise `ValidationError` with exit code 20.

**Step 2: Read Environment Configuration**
- Read the `UE_MAX_OUTPUT_RECORDS` environment variable. If set, parse it as an integer. If not set or unparseable, use the default value of `100`. This is the cap on objects included in STDOUT and Extension Output.

**Step 3: Initialize S3 Client**
- Instantiate a boto3 S3 client using: `aws_access_key_id=input_data.aws_credentials.user`, `aws_secret_access_key=input_data.aws_credentials.password`, `region_name=input_data.aws_region`.

**Step 4: Retrieve All Objects with Pagination**
- Call `list_objects_v2` with `Bucket=bucket_name`. Paginate using `ContinuationToken` until `IsTruncated` is `False` in the response, accumulating all object records into a single list. Each object record contains: `Key` (str), `Size` (int, bytes), `LastModified` (datetime).
- Record `total_object_count` as the length of the complete accumulated list.

**Step 5: Apply Output Cap**
- If `total_object_count > cap`: set `truncated = True`, slice the object list to the first `cap` entries.
- If `total_object_count <= cap`: set `truncated = False`, use the full object list.
- `returned_object_count` = length of the (possibly truncated) object list.

**Step 6: Format Object Records**
- For each object in the (possibly truncated) list, produce a display row:
  - `Key`: the object's S3 key as-is
  - `Size`: convert the integer byte count to a human-readable string using the Size Formatting utility (see Utility Modules)
  - `Last Modified`: format the `LastModified` datetime as an ISO 8601 string (e.g., `2026-09-24T10:00:00Z`; use UTC)

**Step 7: Print STDOUT Table**
- Format the display rows using `tabulate` with `tablefmt="rounded_outline"` and headers `["Key", "Size", "Last Modified"]`.
- Print the resulting table to STDOUT.
- If `truncated` is `True`, print a note on a new line below the table: `NOTE: Output capped at <cap> objects. Total objects in bucket: <total_object_count>.`

**Step 8: Emit STDERR Warning (if truncated)**
- If `truncated` is `True`, write to STDERR: `WARNING: Bucket contains <total_object_count> objects; output capped at <cap> by UE_MAX_OUTPUT_RECORDS`

**Step 9: Populate Output Fields**
- Set `output_data.status` = `"Success: Listed <returned_object_count> objects in <bucket_name>"`
- Set `output_data.result` = `"<returned_object_count> objects found"`

**Step 10: Return Extension Output JSON**
- Build the result object (see Output Examples below) and return with exit code `0`.

### Output Examples

**STDOUT** (2 objects, not truncated):
```
╭──────────────────────────┬──────────┬──────────────────────────╮
│ Key                      │ Size     │ Last Modified            │
├──────────────────────────┼──────────┼──────────────────────────┤
│ reports/report.csv       │ 1.2 MB   │ 2026-09-24T10:00:00Z     │
│ data/archive.zip         │ 45.3 MB  │ 2026-09-22T15:30:00Z     │
╰──────────────────────────┴──────────┴──────────────────────────╯
```

**STDOUT** (truncated, cap=100, total=350):
```
╭──────────────────────────┬──────────┬──────────────────────────╮
│ Key                      │ Size     │ Last Modified            │
├──────────────────────────┼──────────┼──────────────────────────┤
│ reports/report.csv       │ 1.2 MB   │ 2026-09-24T10:00:00Z     │
│ ...                      │ ...      │ ...                      │
╰──────────────────────────┴──────────┴──────────────────────────╯
NOTE: Output capped at 100 objects. Total objects in bucket: 350.
```

**Extension Output result object (JSON)**:

> Note: The full Extension Output also includes `exit_code`, `status_description`, and `invocation` elements that are added automatically during implementation time. Only the `result` element is shown below.

```json
{
  "result": {
    "bucket": "my-demo-bucket",
    "total_object_count": 350,
    "returned_object_count": 100,
    "truncated": true,
    "objects": [
      {"key": "reports/report.csv", "size": "1.2 MB", "last_modified": "2026-09-24T10:00:00Z"},
      {"key": "data/archive.zip", "size": "45.3 MB", "last_modified": "2026-09-22T15:30:00Z"}
    ]
  }
}
```

### Success Criteria
- The `list_objects_v2` API call (and all pagination calls) complete without error.
- Zero or more objects returned is a valid success (an empty bucket is acceptable).
- STDOUT table is printed with correct columns and `rounded_outline` format.
- `output_data.status` and `output_data.result` are populated.
- Extension Output JSON contains `bucket`, `total_object_count`, `returned_object_count`, `truncated`, and `objects` list.
- Return code is `0`.

---

## Action 2: Upload File

**Description**: Connects to AWS S3 using the provided credentials and region, reads the specified local file from the UAC agent host filesystem, and uploads it to the specified S3 bucket at the given S3 object key. On success, captures the ETag from the API response and surfaces it as the result. File handles are managed with context managers to guarantee cleanup.

### Input Requirements

- **action** — must be `Upload File`
- **aws_credentials** — IAM access key ID (`credential.user`) and secret access key (`credential.password`)
- **aws_region** — target AWS region
- **bucket_name** — name of the S3 bucket to upload to
- **local_file** — absolute path to the local file on the agent host
- **s3_object_key** — target object key within the S3 bucket

### Execution Flow

**Step 1: Input Validation**
- Verify aws_credentials is provided and both `user` and `password` are non-empty. If invalid, raise `ValidationError` with exit code 20.
- Verify aws_region, bucket_name, local_file, and s3_object_key are all non-empty strings. If any is missing, raise `ValidationError` with exit code 20.

**Step 2: Validate Local File Existence**
- Check that the path specified by `local_file` exists on the agent host filesystem and is a file (not a directory). If the path does not exist or is not a file, raise `LocalFileNotFoundError` with exit code 1 and status description `"Error: Local file not found — <local_file>"`. Do not proceed to the API call.

**Step 3: Initialize S3 Client**
- Instantiate a boto3 S3 client using: `aws_access_key_id=input_data.aws_credentials.user`, `aws_secret_access_key=input_data.aws_credentials.password`, `region_name=input_data.aws_region`.

**Step 4: Upload File**
- Open the local file in binary read mode (`"rb"`) using a context manager (`with` statement) to guarantee the file handle is closed on both success and failure.
- Inside the context manager, call `put_object` with: `Bucket=bucket_name`, `Key=s3_object_key`, `Body=file_handle`.
- Extract the `ETag` value from the API response dictionary.

**Step 5: Construct Output Values**
- Determine `filename` = the basename of `local_file` (e.g., for `/home/agent/data/report.csv`, `filename` = `report.csv`).
- Construct `s3_uri` = `"s3://<bucket_name>/<s3_object_key>"`.
- `etag` = the ETag string exactly as returned by the S3 API (may include surrounding quotes, e.g., `"d41d8cd98f00b204e9800998ecf8427e"`).

**Step 6: Print STDOUT Confirmation**
- Print to STDOUT: `Uploaded <filename> to <s3_uri> (ETag: <etag>)`

**Step 7: Populate Output Fields**
- Set `output_data.status` = `"Success: Uploaded <filename> to <s3_uri>"`
- Set `output_data.result` = `"ETag: <etag>"`

**Step 8: Return Extension Output JSON**
- Build the result object (see Output Examples below) and return with exit code `0`.

### Output Examples

**STDOUT**:
```
Uploaded report.csv to s3://my-demo-bucket/reports/report.csv (ETag: "d41d8cd98f00b204e9800998ecf8427e")
```

**Extension Output result object (JSON)**:

> Note: The full Extension Output also includes `exit_code`, `status_description`, and `invocation` elements that are added automatically during implementation time. Only the `result` element is shown below.

```json
{
  "result": {
    "s3_uri": "s3://my-demo-bucket/reports/report.csv",
    "etag": "\"d41d8cd98f00b204e9800998ecf8427e\""
  }
}
```

### Success Criteria
- The local file exists and is readable.
- The `put_object` API call completes without error and returns a response containing an `ETag`.
- STDOUT confirmation message is printed.
- `output_data.status` and `output_data.result` are populated.
- Extension Output JSON contains `s3_uri` and `etag`.
- Return code is `0`.

---

# Progress Reporting

Progress Reporting (percentage of completion report) is not required. A single success or failure status message is sufficient for this MVP implementation.

---

# Dynamic Choice Field Population

No Dynamic choice fields should be implemented.

---

# Cancellation Behavior

Default cancellation behavior is used (TERM signal). No custom cancellation logic is required. When UAC cancels the task instance, the TERM signal is sent to the Python process and the process exits immediately. No special cleanup or state management is needed beyond the automatic cleanup provided by Python context managers already in use for file handles.

---

# Re-Run Behavior

Re-runs are treated as initial executions. Both actions are idempotent:
- **List Objects**: Re-running always fetches the current bucket state at the time of execution.
- **Upload File**: Re-running overwrites the object at the specified S3 key if it already exists; the S3 API treats this as a standard `put_object` call.

No special re-run logic is required and no output fields are used to carry state across runs.

---

# Dynamic Commands

No Dynamic commands should be implemented.

---

# Utility Modules

## Required Utility Modules

### 1. Size Formatter

**Purpose:** Converts a raw integer byte count into a human-readable string with appropriate unit suffix, used for the `Size` column in the List Objects STDOUT table.

**Required Capabilities:**
- Accept an integer representing file size in bytes
- Return a formatted string with exactly one decimal place and the appropriate unit suffix
- Unit thresholds (binary, 1024-based):
  - `< 1,024 bytes` → format as `"<N> B"` (no decimal, e.g., `"512 B"`)
  - `>= 1,024 and < 1,048,576` → format as `"<N.N> KB"` (e.g., `"10.5 KB"`)
  - `>= 1,048,576 and < 1,073,741,824` → format as `"<N.N> MB"` (e.g., `"1.2 MB"`)
  - `>= 1,073,741,824` → format as `"<N.N> GB"` (e.g., `"2.3 GB"`)

**Used By:** List Objects action (Step 6: Format Object Records)

---

### 2. AWS S3 Utility

**Purpose:** Encapsulates all boto3 S3 API interactions, providing a clean interface for actions to perform S3 operations without direct boto3 API calls in action code.

**Required Capabilities:**

**S3 Client Initialization:**
- Accept `access_key_id` (str), `secret_access_key` (str), and `region_name` (str) as parameters
- Initialize and return a configured boto3 S3 client bound to the specified region and credentials

**Object Listing (for List Objects action):**
- Accept `bucket_name` (str) as parameter
- Call `list_objects_v2` with pagination: issue successive calls using `ContinuationToken` from each response until `IsTruncated` is `False`
- Accumulate all object records across all pages into a single list
- Each record in the returned list must contain: `key` (str), `size_bytes` (int), `last_modified` (timezone-aware datetime)
- Return the complete list of all object records and the total count

**File Upload (for Upload File action):**
- Accept `bucket_name` (str), `s3_object_key` (str), and `file_handle` (binary file-like object) as parameters
- Call `put_object` with `Bucket`, `Key`, and `Body` parameters
- Return the `ETag` value from the API response as a string

**Error Classification:**
- Catch `botocore.exceptions.ClientError` exceptions and inspect the `Error.Code` in the response to classify:
  - `InvalidClientTokenId` or `SignatureDoesNotMatch` → re-raise as `AuthenticationError`
  - `AccessDenied` → re-raise as `AuthorizationError`
  - `NoSuchBucket` → re-raise as `BucketNotFoundError`
  - All other `ClientError` codes → re-raise as `S3ApiError` including the error code and message
- Catch `botocore.exceptions.EndpointConnectionError` or `botocore.exceptions.ConnectTimeoutError` → re-raise as `ConnectionError`

**Used By:** List Objects action (Steps 3–4), Upload File action (Steps 3–4)

---

## Exception Mapping Strategy

**Authentication and Authorization Errors:**
- AWS `InvalidClientTokenId` error code → `AuthenticationError` (exit code 1, non-transient, user configuration error)
- AWS `SignatureDoesNotMatch` error code → `AuthenticationError` (exit code 1, non-transient, user configuration error)
- AWS `AccessDenied` error code → `AuthorizationError` (exit code 1, non-transient, IAM policy error)

**S3 Resource Errors:**
- AWS `NoSuchBucket` error code → `BucketNotFoundError` (exit code 1, non-transient, user input error)
- Local file does not exist or is not a file → `LocalFileNotFoundError` (exit code 1, non-transient, user input error)

**Network and Connectivity Errors:**
- `botocore.exceptions.EndpointConnectionError` → `ConnectionError` (exit code 1, potentially transient)
- `botocore.exceptions.ConnectTimeoutError` → `ConnectionError` (exit code 1, potentially transient)

**General S3 API Errors:**
- Any other `botocore.exceptions.ClientError` → `S3ApiError` (exit code 1, includes AWS error code and message)

**Validation Errors:**
- Missing or empty required input field → `ValidationError` (exit code 20, non-transient, user input error)

**Unexpected Errors:**
- Any other unhandled exception → `UnexpectedError` (exit code 1, system error)

**Exit Code Guide:**
- Exit code `0`: Successful execution
- Exit code `1`: Operational error — authentication, authorization, resource not found, network, or API error
- Exit code `20`: Input validation error — required field missing or empty; detected before any API call

**Status Description Patterns (for all error scenarios):**
- `AuthenticationError` → `"Error: Authentication failed — <AWS error message>"`
- `AuthorizationError` → `"Error: Access denied — <AWS error message>"`
- `BucketNotFoundError` → `"Error: Bucket not found — <bucket_name>"`
- `LocalFileNotFoundError` → `"Error: Local file not found — <local_file>"`
- `ConnectionError` → `"Error: Connection failed — <error detail>"`
- `S3ApiError` → `"Error: S3 API error — <AWS error code>: <AWS error message>"`
- `ValidationError` → `"Data Validation Error: <field description> is required"`
- `UnexpectedError` → `"Error: Unexpected error — <exception message>"`

---

# Dependencies

## 1. External API Dependencies

**1. AWS S3 (Amazon Simple Storage Service)**
- **Endpoint**: `https://s3.<region>.amazonaws.com`
- **Purpose**: Cloud object storage service; used to list bucket objects and upload files
- **Protocol**: HTTPS
- **Method**: GET (list), PUT (upload) — invoked via boto3 SDK (not raw HTTP)
- **Authentication**: AWS Signature Version 4; access key ID and secret access key supplied from UAC Credential field
- **Response Format**: XML (parsed transparently by boto3 into Python dicts)
- **Data Retrieved/Sent**:
  - List Objects: retrieves object Key, Size (bytes), LastModified (datetime) per object
  - Upload File: sends file binary body; receives ETag in response

**General API Requirements:**
- AWS IAM user must have the following permissions on the target bucket: `s3:ListBucket` (for List Objects), `s3:PutObject` (for Upload File)
- Credentials configured via UAC Credential field (no AWS CLI config files required on the agent)

---

## 2. Python version dependency

Python `>= 3.11` is required.

---

## 3. Target Platform

Linux (x86_64). C extension modules with a confirmed `manylinux_2_17_x86_64` wheel are viable in addition to pure-Python modules. All selected dependencies for this extension are pure-Python, so this constraint is satisfied trivially and the bundle is platform-agnostic.

---

## 4. Python Library Dependencies

**1. boto3**
- **Purpose**: Official AWS SDK for Python; provides the S3 client used for all S3 API operations
- **Version**: `==1.43.102`
- **Installation**: `pip install boto3==1.43.102`
- **Usage**: Used in the AWS S3 Utility module to create the S3 client and call `list_objects_v2` and `put_object`
- **Features Used**: `boto3.client("s3")`, `list_objects_v2`, `put_object`

**2. botocore**
- **Purpose**: Core AWS library that is a direct dependency of boto3; handles HTTP request signing and AWS authentication
- **Version**: `==1.43.102`
- **Installation**: `pip install botocore==1.43.102`
- **Usage**: Installed as a boto3 dependency; provides `botocore.exceptions.ClientError`, `botocore.exceptions.EndpointConnectionError`, `botocore.exceptions.ConnectTimeoutError` for error classification
- **Features Used**: Exception classes for error handling

**3. s3transfer**
- **Purpose**: boto3 dependency that manages efficient S3 data transfers
- **Version**: `==0.19.2`
- **Installation**: `pip install s3transfer==0.19.2`
- **Usage**: Installed as a boto3 dependency; no direct usage in extension code
- **Features Used**: Used internally by boto3

**4. jmespath**
- **Purpose**: boto3 dependency; JSON query language used internally by boto3 for response parsing
- **Version**: `==1.1.0`
- **Installation**: `pip install jmespath==1.1.0`
- **Usage**: Installed as a boto3 dependency; no direct usage in extension code
- **Features Used**: Used internally by boto3

**5. python-dateutil**
- **Purpose**: boto3 dependency; parses ISO 8601 date/time values from S3 metadata responses
- **Version**: `==2.9.0`
- **Installation**: `pip install python-dateutil==2.9.0`
- **Usage**: Installed as a boto3 dependency; no direct usage in extension code
- **Features Used**: Used internally by boto3/botocore for datetime parsing

**6. tabulate**
- **Purpose**: Formats the List Objects result as a `rounded_outline` ASCII table for STDOUT output
- **Version**: `==0.10.0`
- **Installation**: `pip install tabulate==0.10.0`
- **Usage**: Used in the List Objects action (Step 7) to render the object listing table
- **Features Used**: `tabulate(rows, headers=..., tablefmt="rounded_outline")`

---

## 5. Python Standard Library Dependencies

**1. os**
- **Purpose**: Access environment variables and filesystem path operations
- **Version**: Standard library (Python 3.11+)
- **Installation**: No installation required
- **Usage**: Read `UE_MAX_OUTPUT_RECORDS` environment variable (`os.environ.get`); validate local file existence (`os.path.isfile`)
- **Features Used**: `os.environ.get`, `os.path.isfile`, `os.path.basename`

**2. datetime**
- **Purpose**: Format `LastModified` datetime objects from S3 responses as ISO 8601 strings
- **Version**: Standard library (Python 3.11+)
- **Installation**: No installation required
- **Usage**: Used in List Objects action (Step 6) to format the `last_modified` display value
- **Features Used**: `datetime.strftime` or `datetime.isoformat` for UTC formatting

---

## 6. CLI Tool Dependencies

No Dependencies.

---

## 7. Environment Variables

**`UE_MAX_OUTPUT_RECORDS`** (integer, optional):
- **Purpose**: Maximum number of S3 objects included in STDOUT output and Extension Output JSON for the List Objects action. Acts as a safety net to prevent large bucket listings from bloating the UAC database.
- **Default**: `100` (applied when the variable is not set or is not a valid integer)
- **Usage**: Read at the start of the List Objects action execution (Step 2); controls the cap applied in Step 5
- **Examples**: `50`, `100`, `200`
