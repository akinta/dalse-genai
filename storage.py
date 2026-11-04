# json converts Python data into JSON and back again.
import json

# Path helps us work with file paths across operating systems.
from pathlib import Path


# Store the default JSON filename beside this Python file.
DEFAULT_FILE = Path(__file__).with_name("trainees.json")


# def load_trainees(file_path=DEFAULT_FILE):
#     """
#     Load trainee records from a JSON file.

#     Return an empty list if the file does not exist.
#     Raise ValueError if the file contains invalid JSON
#     or an invalid top-level data structure.
#     """

#     # Convert the supplied path into a Path object.
#     path = Path(file_path)

#     # A missing file is treated as an empty database.
#     if not path.exists():
#         return []

#     try:
#         # Open the file in read mode using UTF-8 encoding.
#         with path.open("r", encoding="utf-8") as file:
#             # Convert JSON text into Python objects.
#             data = json.load(file)

#     except json.JSONDecodeError as error:
#         # Give the caller a clear error for malformed JSON.
#         raise ValueError(
#             f"Invalid JSON in {path}: {error}"
#         ) from error

#     # The application expects a list of trainee dictionaries.
#     if not isinstance(data, list):
#         raise ValueError("Trainee data must be a JSON list.")

#     # Check that each record is a dictionary with an ID.
#     for record in data:
#         if not isinstance(record, dict) or not record.get("id"):
#             raise ValueError(
#                 "Each trainee record must be a dictionary with an ID."
#             )

#     # Return the loaded records.
#     return data

def load_trainees(file_path=DEFAULT_FILE):
    """
    Load trainee records from a JSON file.

    Return an empty list if the file does not exist
    or contains no data.
    """

    path = Path(file_path)

    if not path.exists():
        return []

    # if not path.is_file():
    #     raise ValueError(f"{path} is not a file.")

    try:
        with path.open("r", encoding="utf-8") as file:

            # Read the file contents.
            content = file.read().strip()

            # Handle an empty file.
            if not content:
                return []

            # if not content.startswith("[") or not content.endswith("]"):
            #     raise ValueError(
            #         f"Invalid JSON in {path}: Expected a JSON list."
            #     )
            # Convert JSON into Python objects.
            data = json.loads(content)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {path}: {error}"
        ) from error

    if not isinstance(data, list):
        raise ValueError("Trainee data must be a JSON list.")

    for record in data:
        if not isinstance(record, dict) or not record.get("id"):
            raise ValueError(
                "Each trainee record must be a dictionary with an ID."
            )
        # for record in data:
        #     if not isinstance(record, dict) or not record.get("id"):
        #         raise ValueError(
        #             "Each trainee record must be a dictionary with an ID."
        #         )

    return data

def save_trainees(trainees, file_path=DEFAULT_FILE):
    """
    Save trainee records to a JSON file.
    """

    # Convert the supplied path into a Path object.
    path = Path(file_path)


    # Create the parent directory if it does not exist.
    path.parent.mkdir(parents=True, exist_ok=True)

    # Open the file in write mode.
    # Write mode creates the file or replaces its old contents.
    with path.open("w", encoding="utf-8") as file:
        # Convert the Python list into readable JSON text.
        json.dump(
            trainees,
            file,
            indent=4,
            ensure_ascii=False
        )
