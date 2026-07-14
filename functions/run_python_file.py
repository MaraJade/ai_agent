import os
import subprocess

# Set up the schema for this function for the AI agent
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working " +
                "directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, " +
                        "relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to " +
                            "the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
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
        return f'Error: Cannot execute "{file_path}" as it is outside the ' + \
                'permitted working directory'

    try:
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a ' + \
                    'regular file'
    except Exception as e:
        return f'Error checking target file type: {e}'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    # Create the command to be run
    command = ["python", target_file]
    # If additional args were passed, add them to the command
    if args is not None:
        command.extend(args)

    try:
        output_object = subprocess.run(
            command,
            capture_output=True,
            cwd=working_abs_path,
            timeout=30,
            text=True
        )
    except Exception as e:
        return f'Error: executing Python file: {e}'

    output_string = ''
    if output_object.returncode != 0:
        output_string += f'Process exited with code {output_object.returncode}'
    if len(output_object.stdout) == 0 and len(output_object.stderr) == 0:
        output_string += 'No output produced'
    else:
        output_string += f'STDOUT: {output_object.stdout} ' + \
                        f'STDERR: {output_object.stderr}'

    return output_string
