"""
Utility module for the AWS Object Storage extension.

Provides:
- format_size: Converts a raw byte count to a human-readable string.
- S3Client: Wraps boto3 S3 API calls with pagination and error classification.
"""
import logging
from datetime import datetime, timezone
from typing import Any, BinaryIO

import boto3
import botocore.exceptions

from exceptions import (
    AuthenticationError,
    AuthorizationError,
    BucketNotFoundError,
    ConnectionError,
    S3ApiError,
)

logger = logging.getLogger("UNV")

# Binary unit thresholds
_KB = 1_024
_MB = 1_048_576
_GB = 1_073_741_824


def format_size(size_bytes: int) -> str:
    """
    Convert a raw byte count to a human-readable size string.

    Uses binary (1024-based) thresholds:
      - < 1 KB  → "<N> B"   (no decimal)
      - < 1 MB  → "<N.N> KB"
      - < 1 GB  → "<N.N> MB"
      - >= 1 GB → "<N.N> GB"

    Args:
        size_bytes: File size in bytes (non-negative integer).

    Returns:
        Human-readable size string, e.g. "1.2 MB", "512 B".
    """
    if size_bytes < _KB:
        return "%d B" % size_bytes
    if size_bytes < _MB:
        return "%.1f KB" % (size_bytes / _KB)
    if size_bytes < _GB:
        return "%.1f MB" % (size_bytes / _MB)
    return "%.1f GB" % (size_bytes / _GB)


class S3Client:
    """
    Encapsulates all boto3 S3 API interactions for the extension.

    Initialise once per action invocation with the caller's credentials,
    then call list_objects() or upload_file() as required.  All botocore
    exceptions are caught here and re-raised as domain-specific exceptions
    defined in exceptions.py so that action code stays free of boto3 details.
    """

    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        region_name: str,
    ) -> None:
        """
        Initialise a configured boto3 S3 client.

        Args:
            access_key_id:     AWS Access Key ID.
            secret_access_key: AWS Secret Access Key.
            region_name:       AWS region identifier (e.g. "us-east-1").
        """
        logger.info("Initialising S3 client for region: %s", region_name)
        self._client: Any = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
        )
        logger.debug("S3 client initialised successfully")

    def list_objects(self, bucket_name: str) -> tuple[list[dict[str, Any]], int]:
        """
        Retrieve all objects in an S3 bucket using paginated list_objects_v2.

        Accumulates every page of results into a single list.  Each record
        in the returned list contains:
          - key (str):                    S3 object key
          - size_bytes (int):             object size in bytes
          - last_modified (datetime):     timezone-aware UTC datetime

        Args:
            bucket_name: Name of the S3 bucket to list.

        Returns:
            Tuple of (objects, total_object_count) where objects is a list of
            record dicts and total_object_count is len(objects).

        Raises:
            AuthenticationError:  On InvalidClientTokenId or SignatureDoesNotMatch.
            AuthorizationError:   On AccessDenied.
            BucketNotFoundError:  On NoSuchBucket.
            ConnectionError:      On network-level failures.
            S3ApiError:           On any other botocore ClientError.
        """
        logger.info("Listing objects in bucket: %s", bucket_name)
        objects: list[dict[str, Any]] = []
        kwargs: dict[str, Any] = {"Bucket": bucket_name}

        try:
            while True:
                logger.debug("Calling list_objects_v2 with kwargs: %s", kwargs)
                response = self._client.list_objects_v2(**kwargs)
                contents = response.get("Contents", [])
                logger.debug("Page returned %d object(s)", len(contents))

                for obj in contents:
                    last_modified: datetime = obj["LastModified"]
                    if last_modified.tzinfo is None:
                        last_modified = last_modified.replace(tzinfo=timezone.utc)
                    objects.append(
                        {
                            "key": obj["Key"],
                            "size_bytes": obj["Size"],
                            "last_modified": last_modified,
                        }
                    )

                if not response.get("IsTruncated"):
                    break
                kwargs["ContinuationToken"] = response["NextContinuationToken"]

        except botocore.exceptions.ClientError as exc:
            self._classify_client_error(exc)

        except (
            botocore.exceptions.EndpointConnectionError,
            botocore.exceptions.ConnectTimeoutError,
        ) as exc:
            logger.error("Network error while listing objects: %s", str(exc))
            raise ConnectionError(str(exc)) from exc

        total = len(objects)
        logger.info("Listed %d object(s) in bucket: %s", total, bucket_name)
        return objects, total

    def upload_file(
        self,
        bucket_name: str,
        s3_object_key: str,
        file_handle: BinaryIO,
    ) -> str:
        """
        Upload a binary file-like object to S3 using put_object.

        Args:
            bucket_name:    Target S3 bucket name.
            s3_object_key:  Destination object key within the bucket.
            file_handle:    Opened binary file-like object (mode "rb").

        Returns:
            The ETag string exactly as returned by the S3 API.

        Raises:
            AuthenticationError:  On InvalidClientTokenId or SignatureDoesNotMatch.
            AuthorizationError:   On AccessDenied.
            BucketNotFoundError:  On NoSuchBucket.
            ConnectionError:      On network-level failures.
            S3ApiError:           On any other botocore ClientError.
        """
        logger.info(
            "Uploading file to s3://%s/%s", bucket_name, s3_object_key
        )
        try:
            response = self._client.put_object(
                Bucket=bucket_name,
                Key=s3_object_key,
                Body=file_handle,
            )
            etag: str = response["ETag"]
            logger.info(
                "Upload complete — s3://%s/%s ETag: %s",
                bucket_name,
                s3_object_key,
                etag,
            )
            return etag

        except botocore.exceptions.ClientError as exc:
            self._classify_client_error(exc)

        except (
            botocore.exceptions.EndpointConnectionError,
            botocore.exceptions.ConnectTimeoutError,
        ) as exc:
            logger.error("Network error during upload: %s", str(exc))
            raise ConnectionError(str(exc)) from exc

        # Unreachable — _classify_client_error always raises.
        raise S3ApiError("Unexpected control flow in upload_file")  # pragma: no cover

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _classify_client_error(self, exc: botocore.exceptions.ClientError) -> None:
        """
        Inspect a ClientError response and re-raise an appropriate domain exception.

        This method always raises — it never returns normally.

        Raises:
            AuthenticationError:  On InvalidClientTokenId or SignatureDoesNotMatch.
            AuthorizationError:   On AccessDenied.
            BucketNotFoundError:  On NoSuchBucket.
            S3ApiError:           For all other error codes.
        """
        error = exc.response.get("Error", {})
        code: str = error.get("Code", "")
        message: str = error.get("Message", str(exc))

        logger.error("S3 ClientError — code: %s, message: %s", code, message)

        if code in ("InvalidClientTokenId", "SignatureDoesNotMatch"):
            raise AuthenticationError("%s: %s" % (code, message)) from exc
        if code == "AccessDenied":
            raise AuthorizationError("%s: %s" % (code, message)) from exc
        if code == "NoSuchBucket":
            raise BucketNotFoundError(message) from exc
        raise S3ApiError("%s: %s" % (code, message)) from exc
