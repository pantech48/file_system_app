"""
This module contains the functions for reading the configuration data from the JSON file.
"""
import json
import os
from pathlib import Path


CONFIG_FILE = 'config.json'
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), CONFIG_FILE))
WORKING_DIR = Path(__file__).parent.parent
CLIENT_HOME_DIR = os.path.expanduser("~")
TOKEN_FILE_PATH = os.path.join(CLIENT_HOME_DIR, ".file_system_token")


def read_json(file_path: str = CONFIG_PATH) -> dict:
    """
    Reads and returns the JSON data from the file at the given path.

    :param file_path: The path to the JSON file to read.
    :type file_path: str
    :return: The JSON data read from the file.
    :rtype: dict
    """
    with open(file_path, "r") as f:
        return json.load(f)


def config() -> dict:
    """
    Returns the configuration data.

    :return: The configuration data.
    :rtype: dict
    """
    return _config


_config = read_json()
_config["APP"]["working_directory"] = str(WORKING_DIR)
_config["CLIENT"]["home_directory"] = TOKEN_FILE_PATH

