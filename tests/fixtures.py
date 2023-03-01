import pytest
import os

from config.config_parser import config


# write a fixture that creates file and then deletes it after the test is done
@pytest.fixture
def create_file_for_testing():
    with open('test.txt', 'w') as f:
        f.write('test data')
    yield
    if os.path.exists('test.txt'):
        os.remove('test.txt')


@pytest.fixture
def remove_last_created_file():
    yield
    files = os.listdir(config()['APP']['working_directory'])
    files.sort(key=os.path.getctime)
    os.remove(files[-1])
