import os
import shutil
import datetime
import sys
from pathlib import Path
from typing import Dict

from src.utils import generate_filename
from config.config_parser import config
from logs.logger import logger


class FileSystem:
    @staticmethod
    def create_file(data: str = '') -> None:
        """
        Creates file with randomly generated name in the current working directory with provided data.

        :param data: Optional data to write to the file.
        :type data: str
        :raises FileExistsError: If a file with the generated filename already exists.
        :return: None
        """
        try:
            file_name = generate_filename()
            with open(file_name, 'w') as f:
                f.write(data)
                logger.info(f'File {file_name} was successfully created at path "{os.path.abspath(file_name)}"')
        except FileExistsError:
            logger.exception("File already exists.")
            sys.exit(1)

    @staticmethod
    def delete_file(path: str) -> None:
        """
        Deletes a file or directory at the given path.

        :param path: Path to the file or directory to delete.
        :type path: str
        :raises FileExistsError: If the file or directory does not exist.
        :raises PermissionError: If the user does not have permissions to delete the file or directory.
        :return: None
        """
        try:
            if os.path.isfile(path):
                os.remove(path)
                logger.info(f'File {path} was deleted successfully.')
            elif os.path.exists(path) and os.path.isdir(path):
                shutil.rmtree(path)
                logger.info(f"Folder {path} was deleted successfully.")
        except FileNotFoundError:
            logger.exception(f'File {path} not found.')
            sys.exit(1)
        except PermissionError:
            logger.exception(f'You do not have permissions to delete {path}.')
            sys.exit(1)

    @staticmethod
    def read_file(path: str) -> bytes:
        """
        Reads the contents of a file at the given path.

        :param path: Path to the file to read.
        :type path: str
        :raises FileNotFoundError: If the file does not exist.
        :raises PermissionError: If the user does not have permissions to read the file.
        :return: bytes: The contents of the file as bytes.
        """
        try:
            with open(path, 'rb') as f:
                content = f.read()
                logger.info(f'Content of file {path}:'
                            f'{content}')

                return content
        except FileNotFoundError:
            logger.exception(f'File {path} not found.')
            sys.exit(1)
        except PermissionError:
            logger.exception(f'You do not have permissions to read {path}.')
            sys.exit(1)

    @staticmethod
    def get_metadata(path: str) -> Dict[str, str]:
        """
        Returns metadata about a file at the given path.

        :param path: Path to the file to get metadata for.
        :type path: str
        :raises FileNotFoundError: If the file does not exist.
        :return: dict: A dictionary containing the following metadata:
                        - 'name': The name of the file.
                        - 'format': The file format (extension).
                        - 'size': The file size in bytes.
                        - 'full_path': The absolute path to the file.
                        - 'creation_date': The date the file was created.
                        - 'last_access_date': The date the file was last accessed.
                        - 'modification_date': The date the file was last modified.
        """
        try:
            file_stats = os.stat(path)
            file_name = Path(path).name
            _, file_format = os.path.splitext(path)
            file_size = file_stats.st_size
            creation_date = datetime.datetime.fromtimestamp(file_stats.st_ctime).strftime(config()["UTILS"]["date_format"])
            access_date = datetime.datetime.fromtimestamp(file_stats.st_atime).strftime(config()["UTILS"]["date_format"])
            modification_date = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime(config()["UTILS"]["date_format"])

            return {
                'name': file_name,
                'format': file_format,
                'size': f'{file_size} bytes',
                'full_path': os.path.abspath(path),
                'creation_date': creation_date,
                'last_access_date': access_date,
                'modification_date': modification_date
            }

        except FileNotFoundError:
            logger.exception(f"The file '{path}' does not exist.")
            sys.exit(1)
