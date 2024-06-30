import json
import os


def read_json_file(file_path: str):
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config


def write_json_file(file_path: str, payload):
    with open(file_path, 'w') as f:
        json.dump(payload, f, indent=4)


def read_text_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def read_lines_text_file(file_name):
    with open(file_name) as f:
        payload = f.readlines()

    return payload


def write_to_file(filename: str, text: str) -> str:
    """Write text to a file

    Args:
        filename (str): The name of the file to write to
        text (str): The text to write to the file

    Returns:
        str: A message indicating success or failure
    """
    try:
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        return "File written to successfully."
    except Exception as e:
        return f"Error: {str(e)}"
