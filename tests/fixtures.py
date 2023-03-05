import pytest
import os
import hashlib

from config.config_parser import config


@pytest.fixture
def create_signed_file_for_testing(request):
    sha256_obj = hashlib.sha256()
    sha256_obj.update(b'test data')
    sha256_obj.update(config()["SIGNED_FILE_SYSTEM"]["secret_key"].encode('utf-8'))
    signature = sha256_obj.digest()
    with open(request.param, 'wb') as f:
        f.write(signature)
        f.write(b'test data')
    yield
    if os.path.exists(request.param):
        os.remove(request.param)


@pytest.fixture
def create_file_for_testing():
    with open('test.txt', 'wb') as f:
        f.write(b'test data')
    yield
    if os.path.exists('test.txt'):
        os.remove('test.txt')


@pytest.fixture
def get_name_of_last_created_file():
    files = os.listdir(config()['APP']['working_directory'])
    files.sort(key=os.path.getctime)
    return files[-1]


@pytest.fixture
def remove_last_created_file():
    yield
    files = os.listdir(config()['APP']['working_directory'])
    files.sort(key=os.path.getctime)
    os.remove(files[-1])
