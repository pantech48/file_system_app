import hashlib
import pytest

from file_system.signed_file_service import SignedFileSystem
from config.config_parser import config
from tests.fixtures import create_file_for_testing, remove_last_created_file, get_name_of_last_created_file,\
                            create_signed_file_for_testing


def test_generate_signature():
    sha256_obj = hashlib.sha256()
    sha256_obj.update(b'test data')
    sha256_obj.update(config()["SIGNED_FILE_SYSTEM"]["secret_key"].encode('utf-8'))
    signature = sha256_obj.digest()
    assert SignedFileSystem.generate_signature(b'test data') == signature, "Signature is not generated correctly."


def test_sign_file(create_file_for_testing):
    SignedFileSystem.sign_file('test.txt')
    test_signature = SignedFileSystem.generate_signature(b'test data')
    with open('test.txt', 'rb') as f:
        file_data = f.read()
        assert file_data[:config()['SIGNED_FILE_SYSTEM']['len_bytes_for_hash']] == test_signature, \
            "Signature is not signed correctly."
        assert file_data[config()['SIGNED_FILE_SYSTEM']['len_bytes_for_hash']:] == b'test data', \
            "File data is not signed correctly."
    with pytest.raises(FileNotFoundError):
        SignedFileSystem.sign_file('test1.txt')


def test_create_signed_file(remove_last_created_file):
    file_name = SignedFileSystem.create_file(b'test data')
    test_signature = SignedFileSystem.generate_signature(b'test data')
    with open(file_name, 'rb') as f:
        file_data = f.read()
        assert file_data[:config()['SIGNED_FILE_SYSTEM']['len_bytes_for_hash']] == test_signature, \
            "Signature is not signed correctly."
        assert file_data[config()['SIGNED_FILE_SYSTEM']['len_bytes_for_hash']:] == b'test data', \
            "File data is not correct."


@pytest.mark.parametrize("create_signed_file_for_testing", ["test_signed.txt"], indirect=True)
def test_validate_signature(create_signed_file_for_testing):
    secret_key = config()["SIGNED_FILE_SYSTEM"]["secret_key"]
    assert SignedFileSystem.validate_signature("test_signed.txt", secret_key), "Signature is not valid."
    with pytest.raises(FileNotFoundError):
        SignedFileSystem.validate_signature("test_signed1.txt", secret_key)


@pytest.mark.parametrize("create_signed_file_for_testing", ["test_signed.txt"], indirect=True)
def test_read_signed_file(create_signed_file_for_testing, create_file_for_testing):
    with pytest.raises(ValueError):
        assert SignedFileSystem.read_file("test_signed.txt") == b'test data'
    with pytest.raises(ValueError):
        assert SignedFileSystem.read_file("test_signed.txt", 'asd') == b'test data'
    assert SignedFileSystem.read_file("test_signed.txt", config()["SIGNED_FILE_SYSTEM"]["secret_key"]) == b'test data', \
        "File data is not correct."
    assert SignedFileSystem.read_file('test.txt') == b'test data', "File data is not correct."
