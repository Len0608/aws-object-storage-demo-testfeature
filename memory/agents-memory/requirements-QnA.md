# Requirements Completeness Assessment

The requirements are **Moderate Detail**. The core intent is crisp and well-scoped: a two-action MVP AWS S3 integration using boto3, with all primary input fields already named. What remains open are the output design choices — specifically which object properties the List action should display, how to handle very large bucket listings safely, and what information should surface in the UAC task UI output fields after each action completes.

The requirements clearly establish:
- Extension name and purpose (AWS Object Storage, demo/MVP)
- Two actions: List Objects and Upload File
- Python library: boto3
- Core input fields: AWS Credentials, AWS Region, Bucket Name, Local File, S3 Object Key
- No prefix field needed
- Simplicity as a guiding principle

---

# Platform Compatibility

**Platform Compatibility from Requirements**: Linux (x86_64) — confirmed in `environment.md` (OS: Linux, Architecture: x86_64). The build environment is Linux x86_64, which enables C-extension modules with `manylinux_2_17_x86_64` wheels. All selected modules are pure-Python, so this constraint is satisfied trivially.

**Platform Compatibility Agreement**: Linux (x86_64)

---

# Python Modules and Versions

## Researched Modules

All modules verified via PyPI JSON API against Python 3.11 / `manylinux_2_17_x86_64`.

**boto3**
- **Module Purpose**: AWS SDK for Python — provides the S3 client used for List Objects and Upload File operations
- **Version**: 1.43.102
- **Type**: Pure Python

**botocore**
- **Module Purpose**: Core AWS library (boto3 dependency) — handles HTTP request signing and AWS authentication
- **Version**: 1.43.102
- **Type**: Pure Python

**s3transfer**
- **Module Purpose**: boto3 dependency — manages efficient S3 transfers with built-in retry logic and multipart upload support
- **Version**: 0.19.2
- **Type**: Pure Python

**jmespath**
- **Module Purpose**: boto3 dependency — JSON query language used internally to filter AWS API responses
- **Version**: 1.1.0
- **Type**: Pure Python

**python-dateutil**
- **Module Purpose**: boto3 dependency — parses ISO 8601 date/time values from S3 metadata (e.g., LastModified timestamps)
- **Version**: 2.9.0
- **Type**: Pure Python

**tabulate**
- **Module Purpose**: Formats tabular data as ASCII tables for STDOUT; `rounded_outline` style is recommended in the UAC architecture guide for tabular output
- **Version**: 0.10.0
- **Type**: Pure Python

## Agreed Python Modules and Versions

*[Placeholder — to be confirmed once Q1 is answered]*

| Module Name | Module Purpose | Version | Type |
|---|---|---|---|
| — | — | — | — |

---

# Question Rationale

Four questions address the remaining open decisions. Q1 confirms the Python module set and adds `tabulate` for polished demo output. Q2 and Q3 address what the List Objects action shows and how to safely handle potentially large bucket listings. Q4 covers what appears in the UAC task UI as output-only fields after each action completes. Answering these four questions fully specifies the output design, which is the only meaningful gap in the current requirements.

---

# Clarifying Questions for Requirements Refinement

## Critical Decision Path Questions

**Question 1: Python Modules — boto3 + Output Formatting**

Should `tabulate` be added alongside `boto3` to format the List Objects output as a clean ASCII table in STDOUT?

**Options:**

- **O1 (Recommended):** Use `boto3==1.43.102` + `tabulate==0.10.0`
  Objects are listed in a `rounded_outline` ASCII table (columns: Key | Size | Last Modified), which renders clearly in the UAC console and makes the demo immediately readable.
- **O2:** Use `boto3==1.43.102` only
  Objects listed as plain text (one line per object). Simpler, but less visually impactful in the UAC console.

- **Question Type**: New Discussion Topic
- **Context & Resources**: Both modules are pure-Python and fully compatible with the Linux x86_64 build platform. `tabulate` is one of the most widely-used Python formatting libraries and is explicitly recommended in the UAC architecture guide for tabular STDOUT output. `boto3` is the standard AWS SDK, already required by the requirements. Versions verified via PyPI: [boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) | [tabulate on PyPI](https://pypi.org/project/tabulate/)
- **Question Dependencies**: None. Q2 references O1 of this question for its tabulate-formatted option.
- **Recommended Answer**: O1 — `boto3==1.43.102` + `tabulate==0.10.0`
- **Rationale**: For a demo extension, the visual quality of STDOUT output matters. `tabulate` adds no meaningful overhead (pure Python, ~50 KB) and the `rounded_outline` format renders attractively in UAC's task output view. A clean table makes the extension look professional from the first run.
- **Trade-offs**: O2 is marginally simpler (one fewer dependency) but the plain-text output is harder to scan during a demo or presentation.
- **Requirement Impact**: None
- **User's Answer**: O1 — `boto3==1.43.102` + `tabulate==0.10.0`

---

## Essential Input/Output Questions

**Question 2: List Objects — Object Properties Displayed**

When listing S3 objects, which properties should be displayed per object in STDOUT?

**Options:**

- **O1 (Recommended):** Object Key, Size (human-readable, e.g., "1.2 MB"), Last Modified
  Rendered as a tabulate `rounded_outline` table. The three most useful properties for a demo — lets users see file names, sizes, and freshness at a glance.
- **O2:** Object Key only
  A simple list of object keys (file paths). Easiest to implement, but loses the informational value of size and date.
- **O3:** Object Key, Size, Last Modified, Storage Class, ETag
  Full metadata per object. More complete, but may produce a table too wide for the UAC console to display cleanly.

- **Question Type**: New Discussion Topic
- **Context & Resources**: The S3 `list_objects_v2` API returns per-object: Key, Size (bytes), LastModified, ETag, StorageClass. Human-readable sizes (e.g., "1.2 MB" instead of "1258291 bytes") are a standard Python idiom using simple arithmetic — no extra dependency needed. The full API reference: [list_objects_v2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html)
- **Question Dependencies**: O1 assumes Q1=O1 (tabulate available). If Q1=O2, objects would be formatted as plain-text rows instead of a table, but the same three properties would still be shown.
- **Recommended Answer**: O1 — Key, Size (human-readable), Last Modified
- **Rationale**: Three well-chosen columns give the maximum demo impact without overwhelming the display. Human-readable sizes (KB/MB/GB) are more useful than raw bytes. Keeping the column count to three avoids table wrapping in the UAC console.
- **Trade-offs**: O3 adds ETag and StorageClass, which are rarely needed at a glance and widen the table significantly. O2 is simpler but loses the visual appeal that makes the demo compelling.
- **Requirement Impact**: None
- **User's Answer**: O1 — Key, Size (human-readable), Last Modified

---

**Question 3: Large Output Safety Net for List Objects**

Should the List Objects action cap the number of objects returned in STDOUT and Extension Output?

**Options:**

- **O1 (Recommended):** Apply a cap controlled by the `UE_MAX_OUTPUT_RECORDS` environment variable (default: 100 objects)
  When the cap is reached, a note appears at the bottom of STDOUT and a warning is sent to STDERR showing the total object count in the bucket and the applied limit. The Extension Output JSON includes the truncated object list plus the total count as metadata. The cap can be raised per task by setting `UE_MAX_OUTPUT_RECORDS=500` in the task's environment variables — no code changes required.
- **O2:** Always return all objects (no cap)
  Appropriate for a fully controlled demo bucket with a known small object count. Simpler code, but risks large outputs if the bucket grows unexpectedly.

- **Question Type**: New Discussion Topic
- **Context & Resources**: S3 `list_objects_v2` paginates in batches of up to 1,000 objects per API call; buckets can contain millions of objects. UAC stores STDOUT and Extension Output in its database, so large inline outputs can cause performance issues and database bloat. The `UE_MAX_OUTPUT_RECORDS` environment variable pattern is the standard UAC approach for capping record-based output — described in the UAC architecture guide's "Large Output Safety Net Pattern." The variable is set at the task definition level per task instance, so no code change is needed to adjust the limit.
- **Question Dependencies**: None
- **Recommended Answer**: O1 — `UE_MAX_OUTPUT_RECORDS` cap (default 100)
- **Rationale**: The cap adds approximately five lines of code and makes the extension production-safe from the start. Demo buckets are typically small, so the cap will not affect the demo experience. If the demo bucket has more than 100 objects, operators can set `UE_MAX_OUTPUT_RECORDS=500` in the task's environment variables without touching the extension.
- **Trade-offs**: O2 is simpler to implement and acceptable for a strictly controlled demo. However, O1 is a best-practice default that protects against accidental large outputs with no runtime cost.
- **Requirement Impact**: None
- **User's Answer**: O1 — `UE_MAX_OUTPUT_RECORDS` cap (default 100)

---

**Question 4: UAC UI Output Fields and Upload Action Result**

Which output-only fields should appear in the UAC task instance view, and what information should the Upload File action surface on success?

**Options:**

- **O1 (Recommended):** Two output-only fields:
  1. **Status** — a short action summary visible directly in the UAC task list view (e.g., `"Success: Listed 42 objects in my-bucket"` / `"Success: Uploaded report.csv to s3://my-bucket/reports/report.csv"`)
  2. **Result** — action-specific supporting detail (e.g., `"42 objects found"` for List Objects; `ETag: "d41d8cd98f00b204e9800998ecf8427e"` for Upload File)
- **O2:** One output-only field: **Status** only
  Just the summary line. Simpler, but operators cannot see the ETag or object count without opening the full task log.
- **O3:** Three fields: Status + Object Count (List only) + Uploaded S3 Key (Upload only)
  More granular — dedicated fields for count and key. Uses more output field slots and adds action-specific fields that are empty when the other action runs.

- **Question Type**: New Discussion Topic
- **Context & Resources**: UAC output-only fields appear in the task instance list view and task instance detail panel, giving operators immediate status information without opening logs. The UAC architecture guide recommends 2-3 output fields for most extensions. The ETag from a successful S3 upload uniquely identifies the object version and is useful for downstream integrity verification (a common pattern in automated pipelines). Object count from a List is the most useful single-glance metric for that action.
- **Question Dependencies**: None
- **Recommended Answer**: O1 — Status + Result (two output-only fields)
- **Rationale**: Two fields follow the architecture guide's recommendation and provide the most useful information for both actions without adding template noise. The Status field is the "headline" (always populated, visible in list view), and the Result field is the supporting detail (count for List, ETag for Upload). Both fields serve both actions cleanly.
- **Trade-offs**: O2 is simpler but hides the ETag and count from the task list view. O3 is more granular but adds fields that are only meaningful for one of the two actions, making the template slightly noisy.
- **Requirement Impact**: None
- **User's Answer**: O1 — Status + Result (two output-only fields)
