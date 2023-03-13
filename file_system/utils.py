"""
Utility functions for the file_system module.
"""
import random

from config.config_parser import config
from logs.logger import logger


def generate_filename() -> str:
    """
    Generates a random filename using the characters specified in the configuration data.

    :return: A randomly generated filename.
    :rtype: str
    """
    symbols = config()["UTILS"]["characters_for_generate_filename_function"]
    filename = ''.join(random.choice(symbols) for _ in range(config()["UTILS"]["length_of_generate_filename_func"]))
    return filename


def metadata_str(metadata: dict[str, str]) -> None:
    """
    Prints a formatted string representation of the metadata dictionary.

    :param metadata: A dictionary containing file metadata.
    :type metadata: dict
    :return: None
    """
    for field, data in metadata.items():
        logger.info(f"{field}: {data}")

