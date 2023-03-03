import sys

# todo: resolve import error with sys.path variable in different way
sys.path.append(r"C:\\Users\\YPutrin\\Course_007\\file_system_app")

from config.config_parser import config
from file_system.utils import generate_filename


def test_generate_filename():
    assert len(generate_filename()) == config()["UTILS"]["length_of_generate_filename_func"]
    assert type(generate_filename()) == str
    for char in generate_filename():
        assert char in config()["UTILS"]["characters_for_generate_filename_function"]


