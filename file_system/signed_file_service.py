"""
This module contains the SignedFileSystem class, which is a file system that verifies the signature of files.
"""
import hashlib
import base64
import os

from file_system.file_service import FileSystem


class SignedFileSystem(FileSystem):
    @staticmethod
    def sign_content(content: bytes) -> str:
        """
        Signs the given content with the private key.

        :param content: The content to sign.
        :type content: bytes
        :return: str: The signature as a base64-encoded string.
        """
        file_hash = hashlib.sha256(content).digest()
        signature = base64.b64encode(file_hash)
        return signature.decode()

    @staticmethod
    def verify_signature(path: str, signature: str) -> bool:
        """
        Verifies the signature of the file at the given path.

        :param path: Path to the file to verify the signature of.
        :type path: str
        :param signature: The signature to verify.
        :type signature: str
        :return: bool: True if the signature is valid, False otherwise.
        """
        with open(path, 'rb') as f:
            content = f.read()
            file_hash = hashlib.sha256(content).digest()
            signature = base64.b64decode(signature)
            return signature == file_hash

    @staticmethod
    def read_file(path: str, signature: str = None) -> bytes:
        """
        Reads the contents of a file at the given path and verifies its signature if provided.

        :param path: Path to the file to read.
        :type path: str
        :param signature: The signature to verify (optional).
        :type signature: str
        :raises FileNotFoundError: If the file does not exist.
        :raises PermissionError: If the user does not have permissions to read the file.
        :raises ValueError: If the signature is not valid.
        :return: bytes: The contents of the file as bytes.
        """
        content = super().read_file(path)
        if signature:
            if not SignedFileSystem.verify_signature(path, signature):
                raise ValueError('The signature is not valid.')
        return content


