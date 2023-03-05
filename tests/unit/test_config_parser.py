import sys

sys.path.append(r"C:\\Users\\YPutrin\\Course_007\\file_system_app")

from config.config_parser import config, read_json, _config


def test_read_json():
    assert read_json() == config(), "Config is not read correctly."


def test_config():
    assert type(config()) == dict, "Config is not a dictionary."
    assert config() == _config, "Config is not a singleton."