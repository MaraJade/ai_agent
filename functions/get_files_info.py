import os

# Set up the schema for this function for the AI agent
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to " +
                "the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, " +
                        "relative to the working directory (default is the " +
                        "working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    # Make sure the target directory is with the working directory
    try:
        working_abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(
            os.path.join(working_abs_path, directory)
        )
        valid_target_dir = os.path.commonpath([
                working_abs_path, target_dir
            ]) == working_abs_path
    except Exception as e:
        return f'Error: {e}'

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the ' + \
                'permitted working directory'

    # Ensure the directory is actually a directory
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    files = []
    try:
        for item in os.listdir(target_dir):
            size = os.path.getsize(
                os.path.join(target_dir, item)
            )
            isdir = os.path.isdir(
                os.path.join(target_dir, item)
            )
            files.append(f' - {item}: file_size={size} bytes, is_dir={isdir}')
    except Exception as e:
        return f'Error: {e}'

    return '\n'.join(files)
