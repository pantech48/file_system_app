import sys
import os
import pytest

sys.path.append(r"C:\\Users\\YPutrin\\Course_007\\file_system_app")

from tests.fixtures import create_file_for_testing, remove_last_created_file
from file_system.file_service import FileSystem
from config.config_parser import config


def test_create_file(remove_last_created_file):
    file_counter = len(os.listdir(config()['APP']['working_directory']))
    FileSystem.create_file('test data')
    assert len(os.listdir(config()['APP']['working_directory'])) == file_counter + 1


def test_delete_file(create_file_for_testing):
    FileSystem.delete_file('test.txt')
    assert not os.path.exists('test.txt')


def test_read_file(create_file_for_testing):
    FileSystem.read_file('test.txt')
    assert FileSystem.read_file('test.txt') == b'test data'
    with pytest.raises(Exception):
        FileSystem.read_file('test1.txt')


def test_get_metadata(create_file_for_testing):
    FileSystem.get_metadata('test.txt')
    assert FileSystem.get_metadata('test.txt')['name'] == 'test.txt'
    assert FileSystem.get_metadata('test.txt')['format'] == '.txt'
    assert FileSystem.get_metadata('test.txt')['size'] == "9 bytes"
    with pytest.raises(Exception):
        FileSystem.get_metadata('test1.txt')

