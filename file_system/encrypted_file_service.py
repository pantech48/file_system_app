"""
This module contains the EncryptedFileSystem class that is a file system
that encrypts files with AES encryption.
"""
from file_system.file_service import FileSystem
from Crypto.Cipher import AES

from file_system.utils import generate_filename
from logs.logger import logger
from config.config_parser import config


class EncryptedFileSystem(FileSystem):
    """
    This class is a file system that encrypts files with AES encryption.
    """
    KEY = config()["ENCRYPTED_FILE_SYSTEM"]["AES_key"].encode()

    @staticmethod
    def create_file(data: bytes = '') -> None:
        """
        Creates a file with the provided data and encrypt the data.
        :param data: Data to write to the file.
        :return: None
        """
        file_name = generate_filename()
        logger.info(EncryptedFileSystem.KEY)
        key = EncryptedFileSystem.KEY
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        try:
            with open(file_name, 'wb') as f:
                [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
            logger.info(f"Created file {file_name} with encrypted data.")
        except FileExistsError:
            logger.exception(f"File {file_name} already exists.")
            raise

    @staticmethod
    def read_file(path: str) -> bytes:
        """
        Reads the data from the file at the given path and decrypt the data.
        :param path: Path to the file to read the data from.
        :return: Data from the file at the given path.
        :raises FileNotFoundError: If the file at the given path is not found.
        """
        try:
            with open(path, 'rb') as f:
                logger.info(f"Read file {path} with encrypted data.")
                nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]
            key = EncryptedFileSystem.KEY
            cipher = AES.new(key, AES.MODE_EAX, nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)
            logger.info(f"Decrypted data: {data} of the file {path}.")
            return data
        except FileNotFoundError:
            logger.exception(f"File {path} is not found.")
            raise

