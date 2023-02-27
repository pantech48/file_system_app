import json
import os


CONFIG_FILE = 'config.json'
CONFIG_PATH = os.path.abspath(CONFIG_FILE)


def read_json(file_path=CONFIG_FILE):
    with open(file_path, "r") as f:
        return json.load(f)


def config():
    return _config


_config = read_json()




