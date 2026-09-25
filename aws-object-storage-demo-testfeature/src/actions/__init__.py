"""Actions module — business logic implementations."""

from actions.output import ActionOutput
from actions.list_objects import list_objects
from actions.upload_file import upload_file
from manager import ExtensionManager

extension_manager = ExtensionManager()

# Map action choice values (as they appear in the template) to action functions.
# Keys must match the SingleChoice values used by input_data.action.value.
ACTION_MAPPER = {
    "List Objects": list_objects,
    "Upload File": upload_file,
}
