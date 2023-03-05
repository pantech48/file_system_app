import pytest
import sys

sys.path.append(r"C:\\Users\\YPutrin\\Course_007\\file_system_app")


from config.config_parser import config
from file_system.encrypted_file_service import EncryptedFileSystem
from logs.logger import logger
from tests.fixtures import remove_last_created_file, create_encrypted_aes_file


def test_aes_key():
    key = config()["ENCRYPTED_FILE_SYSTEM"]["AES_key"].encode()
    assert EncryptedFileSystem.KEY == key, "The AES key is not correct."


def test_create_encrypted_file(remove_last_created_file):
    data = b'test data'
    file_path = EncryptedFileSystem.create_file(data)
    with open(file_path, 'rb') as f:
        file_content = f.read()
        assert file_content != data, "The data is not encrypted."
        with pytest.raises(UnicodeDecodeError):
            file_content.decode()


@pytest.mark.parametrize('create_encrypted_aes_file', [b'test data'], indirect=True)
def test_read_encrypted_file(create_encrypted_aes_file):
    file_content = EncryptedFileSystem.read_file('test_encrypted')
    assert file_content == b'test data', "The data is not decrypted."
    with pytest.raises(FileNotFoundError):
        EncryptedFileSystem.read_file('test1.txt')
