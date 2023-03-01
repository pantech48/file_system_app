import sys
import os
import pytest

sys.path.append(r"C:\\Users\\YPutrin\\Course_007\\file_system_app")

from tests.fixtures import create_file_for_testing, remove_last_created_file
from src.file_service import delete_file, read_file, get_metadata, create_file
from config.config_parser import config


def test_create_file(remove_last_created_file):
    file_counter = len(os.listdir(config()['APP']['working_directory']))
    create_file('test data')
    assert len(os.listdir(config()['APP']['working_directory'])) == file_counter + 1


def test_delete_file(create_file_for_testing):
    delete_file('test.txt')
    assert not os.path.exists('test.txt')
    with pytest.raises(FileNotFoundError):
        delete_file('test123.txt')


def test_read_file(create_file_for_testing):
    read_file('test.txt')
    assert read_file('test.txt') == b'test data'
    with pytest.raises(FileNotFoundError):
        read_file('test123.txt')


def test_get_metadata():
    pass