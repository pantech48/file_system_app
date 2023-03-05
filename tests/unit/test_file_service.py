import sys
import os
import pytest

sys.path.append(r"C:\\Users\\YPutrin\\Course_007\\file_system_app")

from tests.fixtures import create_file_for_testing, remove_last_created_file
from file_system.file_service import FileSystem
from config.config_parser import config
from logs.logger import logger


def test_create_file(remove_last_created_file):
    file_storage = FileSystem.FILE_STORAGE_PATH
    logger.info(f"File storage path: {file_storage}")
    file_counter = len(os.listdir(file_storage))
    logger.info(f"File counter: {file_counter}")
    FileSystem.create_file(b'test data')
    assert len(os.listdir(file_storage)) == file_counter + 1, \
        "File was not created."



def test_delete_file(create_file_for_testing):
    FileSystem.delete_file('test.txt')
    assert not os.path.exists('test.txt'), "File was not deleted."


def test_read_file(create_file_for_testing):
    FileSystem.read_file('test.txt')
    assert FileSystem.read_file('test.txt') == b'test data', "File was not read correctly."
    with pytest.raises(Exception):
        FileSystem.read_file('test1.txt')


def test_get_metadata(create_file_for_testing):
    FileSystem.get_metadata('test.txt')
    assert FileSystem.get_metadata('test.txt')['name'] == 'test.txt', "File name is not correct."
    assert FileSystem.get_metadata('test.txt')['format'] == '.txt', "File format is not correct."
    assert FileSystem.get_metadata('test.txt')['size'] == "9 bytes", "File size is not correct."
    with pytest.raises(Exception):
        FileSystem.get_metadata('test1.txt')

