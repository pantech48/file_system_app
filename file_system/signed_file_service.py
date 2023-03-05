"""
This module contains the SignedFileSystem class, which is a file system that verifies the signature of files.
"""
import hashlib
import os

from file_system.file_service import FileSystem
from file_system.utils import generate_filename
from logs.logger import logger
from config.config_parser import config


class SignedFileSystem(FileSystem):
    """
    This class is a file system that verifies the signature of files.
    """
    SECRET_KEY = config()["SIGNED_FILE_SYSTEM"]["secret_key"]

    @staticmethod
    def generate_signature(file_content: bytes) -> bytes:
        """ Generates a signature for the provided file content.
        :param file_content: Content of the file to generate a signature for.
        :return: Signature for the provided file content.
        """
        sha256_obj = hashlib.sha256()
        sha256_obj.update(file_content)
        sha256_obj.update(SignedFileSystem.SECRET_KEY.encode('utf-8'))
        signature = sha256_obj.digest()
        return signature

    @staticmethod
    def sign_file(path: str) -> None:
        """
        Signs a file at the given path.
        :param path: Path to the file to sign.
        :return: None
        :raises FileNotFoundError: If the file at the given path is not found.
        """
        try:
            with open(path, 'rb') as f:
                file_content = f.read()
                signature = SignedFileSystem.generate_signature(file_content)
            with open(path, 'wb')as f:
                f.write(signature)
                f.write(file_content)
        except FileNotFoundError:
            logger.exception(f"File {path} is not found.")
            raise

    @staticmethod
    def validate_signature(path: str, secret_key: str) -> bool:
        """
        Validates the signature of a file at the given path.
        :param path: Path to the file to validate the signature of.
        :param secret_key: Signature to validate.
        :return: True if the signature is valid, False otherwise.
        :raises FileNotFoundError: If the file at the given path is not found.
        """
        try:
            with open(path, 'rb') as f:
                signature_from_open_file = f.read(config()['SIGNED_FILE_SYSTEM']['len_bytes_for_hash'])
                file_content = f.read()
                sha256_obj = hashlib.sha256()
                sha256_obj.update(file_content)
                sha256_obj.update(secret_key.encode('utf-8'))
                computed_signature = sha256_obj.digest()
            return computed_signature == signature_from_open_file
        except FileNotFoundError:
            logger.exception(f"File {path} is not found.")
            raise

    @staticmethod
    def create_file(data: bytes = b'') -> None:
        """ Creates a file with the provided data and signs it.
        :param data: Data to write to the file.
        :return: None
        :raises FileExistsError: If the file already exists.
        """
        try:
            file_name = generate_filename()
            with open(file_name, 'wb') as f:
                signature = SignedFileSystem.generate_signature(data)
                f.write(signature)
                f.write(data)
                logger.info(f'Signed file {file_name} was successfully created at path "{os.path.abspath(file_name)}"')
        except FileExistsError:
            logger.exception("File already exists.")
            raise

    @staticmethod
    def read_file(path, secret_key: str = '') -> bytes:
        """
        Reads the content of a file at the given path.
        :param path: Path to the file to read.
        :param secret_key: If True, the signature of the file will be validated.
        :return: Content of the file at the given path.
        """
        if secret_key:
            if not SignedFileSystem.validate_signature(path, secret_key):
                err_message = "Invalid signature"
                logger.exception(err_message)
                raise ValueError(err_message)
            return super().read_file(path)[config()['SIGNED_FILE_SYSTEM']['len_bytes_for_hash']:]
        else:
            assumed_signature = super().read_file(path)[:config()['SIGNED_FILE_SYSTEM']['len_bytes_for_hash']]
            file_content = super().read_file(path)[config()['SIGNED_FILE_SYSTEM']['len_bytes_for_hash']:]
            if assumed_signature == SignedFileSystem.generate_signature(file_content):
                err_message = "This file is signed, you need to provide secret key to access it."
                logger.exception(err_message)
                raise ValueError(err_message)
            return super().read_file(path)




sf = SignedFileSystem()
f = FileSystem()
#sf.create_file(b'Hello, world!')
FileSystem.read_file(r'C:\Users\YPutrin\Course_007\file_system_app\file_system\08xmm63tvk')

