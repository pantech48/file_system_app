import pytest
import os
import hashlib
from Crypto.Cipher import AES
from pathlib import Path

from config.config_parser import config
from file_system.file_service import FileSystem
from logs.logger import logger


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
def create_encrypted_aes_file(request):
    file_name = 'test_encrypted'
    key = config()["ENCRYPTED_FILE_SYSTEM"]["AES_key"].encode()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(request.param)
    with open(file_name, 'wb') as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
    yield
    if os.path.exists(file_name):
        os.remove(file_name)


@pytest.fixture
def create_file_for_testing():
    with open('test.txt', 'wb') as f:
        f.write(b'test data')
    yield
    if os.path.exists('test.txt'):
        os.remove('test.txt')


@pytest.fixture
def get_name_of_last_created_file():
    file_storage = FileSystem.FILE_STORAGE_PATH
    files = os.listdir(file_storage)
    files.sort(key=os.path.getctime)
    return files[-1]


@pytest.fixture
def remove_last_created_file():
    yield
    file_storage = FileSystem.FILE_STORAGE_PATH
    files = [os.path.join(FileSystem.FILE_STORAGE_PATH, file) for file in os.listdir(file_storage)]
    files.sort(key=os.path.getctime)
    last_created_file = files[-1]
    os.remove(last_created_file)
