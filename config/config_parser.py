import json
import os


CONFIG_FILE = 'config.json'
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), CONFIG_FILE))
print(CONFIG_PATH)


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



