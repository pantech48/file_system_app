import os
import shutil
import datetime
from pathlib import Path

from utils import generate_filename
from config_parser import config


def create_file(data=''):
    with open(generate_filename(), 'w') as f:
        f.write(data)


def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)


# todo: add validation of files
def read_file(path):
    with open(path, 'rb') as f:
        content = f.read()
        return content


def get_metadata(path):
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
