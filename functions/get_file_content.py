import os
from config import MAX_CHARS

# Set up the schema for this function for the AI agent
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Retrieves the content (at most {MAX_CHARS} " +
            "characters) of a specified file within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to " +
                            "the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    # Make sure the target file is with the working directory
    try:
        working_abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_abs_path, file_path)
        )
        valid_target_file = os.path.commonpath([
                working_abs_path, target_file
            ]) == working_abs_path
    except Exception as e:
        return f'Error: {e}'

    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the ' + \
                'permitted working directory'

    # Ensure the file is actually a file
    try:
        if not os.path.isfile(target_file):
            return 'Error: File not found or is not a regular file: ' + \
                f'"{file_path}"'
    except Exception as e:
        return f'Error: {e}'

    # Read the file
    try:
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            # Check if the file was larger than the limit
            if f.read(1):
                content += f'[... File "{file_path}" truncated at ' + \
                    f'{MAX_CHARS} characters]'
    except Exception as e:
        return f'Error: {e}'

    return content
