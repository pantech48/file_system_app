import configparser
import json
import os


CONFIG_FILE = 'config.json'
CONFIG_PATH = os.path.relpath(CONFIG_FILE)


def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def config():
    return read_json(CONFIG_PATH)




