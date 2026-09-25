"""
Exceptions module for UAC Universal Extensions.

This module provides:
- Base ExecutionError class
- Standard exception types (DataValidationError, ConnectionError, etc.)
- AWS S3-specific exception types for boto3 error classification
- Exit code conventions

Exit code guide:
    0  — Successful execution
    1  — Operational error (auth, resource, network, API, unexpected)
    20 — Input validation error (missing or empty required field)
"""
from typing import Optional


class ExecutionError(Exception):
    """
    The default error raised by an extension.

    All extension errors must inherit from it.

    Attrs:
        exit_code: The exit code of the extension (for UAC)
        message: The error message for status description
    """

    exit_code: int = 1
    message: str = "Execution Failed"

    def __init__(self, message: Optional[str] = None):
        """
        Initialize exception.

        Args:
            message: Optional message that will be appended to the default message.

        Note:
            To return result data with errors, use error_manager.set_result()
            before raising the exception.
        """
        if message:
            self.message = f"{self.message}: {message}"

        super().__init__(self.message)


class DataValidationError(ExecutionError):
    """Raised when an input field is invalid."""
    exit_code = 20
    message = "Data Validation Error"


class UnexpectedSystemError(ExecutionError):
    """Raised for unexpected system errors."""
    exit_code = 1
    message = "System Error"


class ValidationError(ExecutionError):
    """
    Raised when a required input field is missing or empty.

    Use before any API call to surface configuration errors early.
    Exit code 20 signals a non-transient user input error to UAC.

    Example:
        raise ValidationError("aws_region is required")
    """
    exit_code = 20
    message = "Data Validation Error"


class AuthenticationError(ExecutionError):
    """
    Raised when AWS credentials are rejected by the S3 API.

    Maps from botocore ClientError codes: InvalidClientTokenId,
    SignatureDoesNotMatch. Indicates a non-transient user
    configuration error (wrong access key ID or secret key).

    Example:
        raise AuthenticationError("InvalidClientTokenId: The AWS Access Key Id you provided does not exist")
    """
    exit_code = 1
    message = "Authentication failed"


class AuthorizationError(ExecutionError):
    """
    Raised when the IAM principal lacks permission for the requested S3 operation.

    Maps from botocore ClientError code: AccessDenied. Indicates a
    non-transient IAM policy error requiring remediation outside the extension.

    Example:
        raise AuthorizationError("AccessDenied: Access Denied")
    """
    exit_code = 1
    message = "Access denied"


class BucketNotFoundError(ExecutionError):
    """
    Raised when the specified S3 bucket does not exist or is not accessible.

    Maps from botocore ClientError code: NoSuchBucket. Indicates a
    non-transient user input error (bucket name typo or wrong region).

    Example:
        raise BucketNotFoundError("my-demo-bucket")
    """
    exit_code = 1
    message = "Bucket not found"


class LocalFileNotFoundError(ExecutionError):
    """
    Raised when the local file path provided for upload does not exist
    on the agent host filesystem or is not a regular file.

    Checked before any S3 API call is made. Indicates a non-transient
    user input error.

    Example:
        raise LocalFileNotFoundError("/home/agent/data/report.csv")
    """
    exit_code = 1
    message = "Local file not found"


class ConnectionError(ExecutionError):
    """
    Raised when a network-level failure prevents reaching the S3 endpoint.

    Maps from botocore exceptions: EndpointConnectionError,
    ConnectTimeoutError. May be transient; the caller can advise retry.

    Example:
        raise ConnectionError("Failed to connect to s3.us-east-1.amazonaws.com")
    """
    exit_code = 1
    message = "Connection failed"


class S3ApiError(ExecutionError):
    """
    Raised for any botocore ClientError not covered by a more specific
    exception class (AuthenticationError, AuthorizationError, BucketNotFoundError).

    Includes the AWS error code and message to aid debugging.

    Example:
        raise S3ApiError("SlowDown: Please reduce your request rate")
    """
    exit_code = 1
    message = "S3 API error"


class UnexpectedError(ExecutionError):
    """
    Raised for any unhandled exception that does not map to a known
    AWS or operational error condition.

    Used as the catch-all in extension_start for non-ExecutionError exceptions.

    Example:
        raise UnexpectedError(str(e))
    """
    exit_code = 1
    message = "Unexpected error"
