from utils import generate_filename
import os
import shutil


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
    ...

