import os
import shutil
import datetime
from pathlib import Path

from utils import generate_filename
from config_parser import config


def create_file(data=''):
    try:
        file_name = generate_filename()
        with open(file_name, 'w') as f:
            f.write(data)
    except FileExistsError:
        print("File already exists.")


def delete_file(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.exists(path) and os.path.isdir(path):
            shutil.rmtree(path)
    except FileExistsError:
        print(f'File {path} not found.')
    except PermissionError:
        print(f'You do not have permissions to delete {path}.')


def read_file(path):
    try:
        with open(path, 'rb') as f:
            content = f.read()
            return content
    except FileExistsError:
        print(f'File {path} not found.')
    except PermissionError:
        print(f'You do not have permissions to read {path}.')


def get_metadata(path):
    try:
        metadata = {}
        file_stats = os.stat(path)
        file_name = Path(path).name
        _, file_format = os.path.splitext(path)
        file_size = file_stats.st_size
        creation_date = datetime.datetime.fromtimestamp(file_stats.st_ctime).strftime(config()["date_format"])
        access_date = datetime.datetime.fromtimestamp(file_stats.st_atime).strftime(config()["date_format"])
        modification_date = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime(config()["date_format"])

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
        print(f"The file '{path}' does not exist.")
