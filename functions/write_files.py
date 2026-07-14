import os

# Set up the schema for this function for the AI agent
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file within the " +
                "working directory (overwriting if the file exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to " +
                            "the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
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
        return f'Error checking target file location: {e}'

    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside ' + \
                'the permitted working directory'

    # Make sure the file isn't a directory
    try:
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
    except Exception as e:
        return f'Error checking target file type: {e}'

    # Get the parent path of the file
    try:
        target_dir = os.path.normpath(
            os.path.join(
                working_abs_path,
                os.path.dirname(file_path)
            )
        )
    except Exception as e:
        return f'Error getting parent dir: {e}'

    # Make sure all the dirs in the file path exist, create them if they don't
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        return f'Error creating directories: {e}'

    try:
        with open(target_file, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error writing to file: {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} ' + \
        'characters written)'
