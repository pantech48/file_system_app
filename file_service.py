import os
import shutil
import datetime

from utils import generate_filename
from pathlib import Path
from config_parser import config


def create_file(data=''):
    with open(generate_filename(), 'w') as f:
        f.write(data)


def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)


def read_file(path):
    with open(path) as f:
        content = f.read()
        return content


def get_metadata(path):
    metadata = {}
    file_stats = os.stat(path)
    file_name = Path(path).name
    file_format = file_name.split('.')[-1]
    file_size = file_stats.st_size
    creation_date = datetime.datetime.fromtimestamp(file_stats.st_ctime).strftime(config()["date_format"])
    access_date = datetime.datetime.fromtimestamp(file_stats.st_atime).strftime(config()["date_format"])
    modification_date = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime(config()["date_format"])

    metadata['name'] = file_name
    metadata['format'] = file_format
    metadata['size'] = f'{file_size} bytes'
    metadata['full_path'] = os.path.abspath(path)
    metadata['creation_date'] = creation_date
    metadata['last_access_date'] = access_date
    metadata['modification_date'] = modification_date

    return metadata
