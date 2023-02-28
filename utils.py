import random
from typing import Dict

from config_parser import config


def generate_filename() -> str:
    """
    Generates a random filename using the characters specified in the configuration data.

    :return: A randomly generated filename.
    :rtype: str
    """
    symbols = config()["characters_for_generate_filename_function"]
    filename = ''.join(random.choice(symbols) for _ in range(config()["length_of_filename"]))
    return filename


def metadata_str(metadata: Dict[str, str]) -> None:
    """
    Prints a formatted string representation of the metadata dictionary.

    :param metadata: A dictionary containing file metadata.
    :type metadata: dict
    :return: None
    """
    for field, data in metadata.items():
        print(field, ": ", data)
