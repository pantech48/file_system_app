import sys
import os
import pytest

sys.path.append(r"C:\\Users\\YPutrin\\Course_007\\file_system_app")

from config.config_parser import config, read_json, _config


def test_read_json():
    assert read_json() == config()


def test_config():
    assert type(config()) == dict
    assert config() == _config