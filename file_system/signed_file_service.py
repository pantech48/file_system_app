"""
This module contains the SignedFileSystem class, which is a file system that verifies the signature of files.
"""
import hashlib
import base64
import os

from file_system.file_service import FileSystem
from file_system.utils import generate_filename
from logs.logger import logger


class SignedFileSystem(FileSystem):
    """
    This class is a file system that verifies the signature of files.
    """
    def __init__(self):
        """
        Initializes the SignedFileSystem class.
        """
        self.private_key = hashlib.sha256().digest()
        self.public_key = base64.b64encode(self.private_key).decode('utf-8')

    def generate_signature(self, file_content: bytes) -> bytes:
        """ Generates a signature for the provided file content.
        :param file_content: Content of the file to generate a signature for.
        :return: Signature for the provided file content.
        """
        file_hash = hashlib.sha256(file_content).digest()
        signature = base64.b64encode(file_hash + self.private_key)
        return signature

    def sign_file(self, path: str) -> None:
        """
        Signs a file at the given path.
        :param path: Path to the file to sign.
        :return: None
        :raises FileNotFoundError: If the file at the given path is not found.
        """
        try:
            with open(path, 'rb') as f:
                file_content = f.read()
                signature = self.generate_signature(file_content)
            with open(path, 'ab')as f:
                f.seek(0, 0)
                f.write(signature)
        except FileNotFoundError:
            logger.exception(f"File {path} is not found.")
            raise

    # todo: for now validation mechanism is not working correctly and needs to be fixed
    def validate_signature(self, path: str) -> bool:
        """
        Validates the signature of a file at the given path.
        :param path: Path to the file to validate the signature of.
        :return: True if the signature is valid, False otherwise.
        :raises FileNotFoundError: If the file at the given path is not found.
        """
        public_key = self.public_key.encode('utf-8')
        try:
            with open(path, 'rb') as f:
                signature_from_open_file = f.readline()
                file_content = f.read()
                file_hash = hashlib.sha256(file_content).digest()
                computed_signature = base64.b64encode(file_hash + public_key)
            return computed_signature == signature_from_open_file.decode('utf-8')
        except FileNotFoundError:
            logger.exception(f"File {path} is not found.")
            raise

    def create_signed_file(self, data: bytes = b'') -> None:
        """ Creates a file with the provided data and signs it.
        :param data: Data to write to the file.
        :return: None
        :raises FileExistsError: If the file already exists.
        """
        try:
            file_name = generate_filename()
            with open(file_name, 'wb') as f:
                signature = self.generate_signature(data)
                f.write(signature)
                f.write(data)
                logger.info(f'File {file_name} was successfully created at path "{os.path.abspath(file_name)}"')
        except FileExistsError:
            logger.exception("File already exists.")
            raise

    def read_signed_file(self, path, signature: bool = True):
        """
        Reads the content of a file at the given path.
        :param path: Path to the file to read.
        :param signature: If True, the signature of the file will be validated.
        :return: Content of the file at the given path.
        """
        content = super().read_file(path)

        if signature:
            if not self.validate_signature(path):
                raise ValueError("Invalid signature")
        return content


