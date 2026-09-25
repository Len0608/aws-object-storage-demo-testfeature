"""ActionOutput dataclass for action return values."""

from dataclasses import dataclass
from typing import Optional, Any, Dict, List


@dataclass
class ActionOutput:
    """Output from action functions.

    Carries the structured result data that is serialised into the Extension
    Output JSON (unv_output).  Two result shapes are supported:

    List Objects result keys:
        bucket               (str)  — S3 bucket name
        total_object_count   (int)  — total objects in the bucket (all pages)
        returned_object_count (int) — objects actually included in the output
        truncated            (bool) — True when output was capped
        objects              (list) — list of {"key", "size", "last_modified"} dicts

    Upload File result keys:
        s3_uri  (str) — s3://<bucket>/<key>
        etag    (str) — ETag returned by the S3 API
    """

    # -----------------------------------------------------------------
    # List Objects fields
    # -----------------------------------------------------------------
    bucket: Optional[str] = None
    total_object_count: Optional[int] = None
    returned_object_count: Optional[int] = None
    truncated: Optional[bool] = None
    objects: Optional[List[Dict[str, Any]]] = None

    # -----------------------------------------------------------------
    # Upload File fields
    # -----------------------------------------------------------------
    s3_uri: Optional[str] = None
    etag: Optional[str] = None

    # -----------------------------------------------------------------
    # Control fields
    # No stdout_options / output_options choice fields are defined in the
    # template for this extension — STDOUT printing is handled directly
    # inside each action function; to_dict() always includes all fields.
    # -----------------------------------------------------------------
    stdout_options: List[str] = None
    output_options: List[str] = None

    def __post_init__(self):
        """Initialise control fields with defaults."""
        if self.stdout_options is None:
            self.stdout_options = []
        if self.output_options is None:
            self.output_options = []

    def print_output(self):
        """Print to STDOUT.

        STDOUT output for both actions is produced directly within each action
        function before ActionOutput is returned.  This method is therefore a
        no-op; it exists to satisfy the ActionOutput contract expected by
        extension.py.
        """

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for Extension Output (unv_output).

        Builds the result sub-object included in the extension output JSON.
        The shape depends on which fields are populated:

        - List Objects path: bucket, total_object_count, returned_object_count,
          truncated, objects are all set.
        - Upload File path: s3_uri and etag are set.
        """
        output: Dict[str, Any] = {}

        # List Objects result
        if self.bucket is not None:
            output["bucket"] = self.bucket
        if self.total_object_count is not None:
            output["total_object_count"] = self.total_object_count
        if self.returned_object_count is not None:
            output["returned_object_count"] = self.returned_object_count
        if self.truncated is not None:
            output["truncated"] = self.truncated
        if self.objects is not None:
            output["objects"] = self.objects

        # Upload File result
        if self.s3_uri is not None:
            output["s3_uri"] = self.s3_uri
        if self.etag is not None:
            output["etag"] = self.etag

        return output
