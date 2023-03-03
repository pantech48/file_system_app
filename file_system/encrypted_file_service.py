"""
This module contains the EncryptedFileSystem class that is a file system
that encrypts files before writing them to disk.
"""
from file_system.file_service import FileSystem


class EncryptedFileSystem(FileSystem):
    def __init__(self):
        pass