# Test Environment Setup Guide

**Extension:** AWS Object Storage (aws-object-storage-demo-testfeature)
**Actions covered:** List Objects, Upload File

---

## 🌐 EXTERNAL SERVICE SETUP: AWS S3

BEFORE RUNNING TESTS, CREATE THE FOLLOWING ON THE EXTERNAL SERVICE:

---

### 1. S3 Bucket

- **What:** An existing S3 bucket in a single AWS region that the test tasks will target.
- **Why:** Both the `List Objects` and `Upload File` actions require a real, pre-existing bucket. Neither action creates the bucket — if the bucket is absent, the extension raises `BucketNotFoundError` and the task fails with exit code 1.
- **How:**
  1. Log in to the [AWS Console](https://console.aws.amazon.com/s3) or use the AWS CLI.
  2. Create a bucket with a name that satisfies S3 naming rules (lowercase, 3–63 characters, no underscores).
  3. Note the **bucket name** and the **AWS region** (e.g., `us-east-1`). Both will be entered as task field values.
  4. Leave default access settings (Block Public Access enabled) — the extension uses private IAM access.
- **Example:**
  ```
  Bucket name: ue-test-aws-s3-demo
  Region:      us-east-1
  ```

---

### 2. IAM User with Programmatic Access

- **What:** An AWS IAM user that has an access key ID and secret access key for API authentication.
- **Why:** The extension authenticates to AWS using credentials stored in a UAC Credential record. It reads `credential.user` as the Access Key ID and `credential.password` as the Secret Access Key. No AWS CLI config or instance roles are used.
- **How:**
  1. In the AWS Console navigate to **IAM → Users → Create user**.
  2. Attach an inline or managed policy granting at minimum the permissions listed in item 3 below.
  3. Under **Security credentials**, create an **Access key** (type: *Other*).
  4. Copy and store the **Access Key ID** and **Secret Access Key** — the secret is shown only once.
- **Example:**
  ```
  Access Key ID:     AKIAIOSFODNN7EXAMPLE
  Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
  ```

---

### 3. IAM Policy — Required S3 Permissions

- **What:** An IAM policy granting `s3:ListBucket` and `s3:PutObject` on the test bucket.
- **Why:**
  - `List Objects` action calls `s3:ListBucket` — absent permission returns `AccessDenied`.
  - `Upload File` action calls `s3:PutObject` — absent permission returns `AccessDenied`.
- **How:** Attach the following inline policy to the IAM user created in item 2:
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:ListBucket"
        ],
        "Resource": "arn:aws:s3:::ue-test-aws-s3-demo"
      },
      {
        "Effect": "Allow",
        "Action": [
          "s3:PutObject"
        ],
        "Resource": "arn:aws:s3:::ue-test-aws-s3-demo/*"
      }
    ]
  }
  ```
  Replace `ue-test-aws-s3-demo` with the actual bucket name.

---

### 4. UAC Credential Record

- **What:** A UAC Credential record that stores the IAM access key so the extension can reference it via the `aws_credentials` field.
- **Why:** UAC Credential fields return a Credential object; the extension reads `credential.user` (Access Key ID) and `credential.password` (Secret Access Key). A plain text field cannot supply these values.
- **How:**
  1. In the UAC UI navigate to **Configuration → Credentials → Create Credential**.
  2. Set **Type** to *Username / Password*.
  3. Enter the IAM **Access Key ID** in the **Username** field.
  4. Enter the IAM **Secret Access Key** in the **Password** field.
  5. Give the credential a recognisable name (e.g., `aws-s3-test-creds`).
  6. Save the record.
- **Example:**
  ```
  Credential name: aws-s3-test-creds
  Username field:  AKIAIOSFODNN7EXAMPLE        ← Access Key ID
  Password field:  wJalrXUtnFEMI/K7MDENG/...  ← Secret Access Key
  ```

---

## 🖥️ AGENT HOST SETUP

BEFORE RUNNING TESTS, PREPARE THE FOLLOWING ON THE UAC AGENT MACHINE:

---

### 1. Test Input File for Upload File Action

- **What:** A readable file at a known absolute path on the UAC agent host.
- **Why:** The `Upload File` action validates that the path supplied in the `local_file` field exists and is a regular file before calling the S3 API. If the file is absent the extension raises `LocalFileNotFoundError` (exit code 1) without making an API call.
- **How:** Log in to the agent host and run the following command to create a minimal test file:
  ```bash
  mkdir -p ~/ue-test-data && echo "ue-s3-upload-test" > ~/ue-test-data/test-upload.txt
  ```
  This creates the file at `~/ue-test-data/test-upload.txt`.  
  Supply the **absolute** path (e.g., `/home/<agent-user>/ue-test-data/test-upload.txt`) in the `local_file` task field.
- **Example:**
  ```
  Absolute path: /home/agent/ue-test-data/test-upload.txt
  Content:       ue-s3-upload-test
  ```

---

## 📋 CHECKLIST

  ☐ S3 bucket created in the target region
  ☐ IAM user created with programmatic access (access key ID + secret access key noted)
  ☐ IAM policy granting `s3:ListBucket` and `s3:PutObject` on the test bucket attached to the IAM user
  ☐ UAC Credential record created with Access Key ID in Username and Secret Access Key in Password
  ☐ Test upload file created on the agent host at an absolute path under the home directory
  ☐ Verified: `aws s3 ls s3://<bucket-name>` returns successfully using the test credentials (optional pre-check)
