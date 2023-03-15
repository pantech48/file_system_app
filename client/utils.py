""" Module with request functions """
import requests

from config.config_parser import config
from logs.logger import logger


LOCAL_HOST = config()["ROUTES"]["local_host"]
TOKEN_FILE_PATH = config()["CLIENT"]["home_directory"]


def sign_up(username: str, password: str, email: str) -> requests.Response:
    url = f"{LOCAL_HOST}/user"
    payload = {'username': username, 'password': password, 'email': email}
    response = requests.post(url, json=payload)
    return response.json()


def sign_in(username: str, password: str) -> requests.Response:
    url = f"{LOCAL_HOST}/login"
    response = requests.get(url, auth=(username, password))
    return response.json()


def upload_file(filename: str):
    try:
        with open(filename, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        logger.exception("File not found.")
        raise
    url = f"{LOCAL_HOST}/files"
    payload = {'content': content}
    response = requests.post(url, json=payload)
    return response.json()


def download_file(filename: str):
    url = f"{LOCAL_HOST}/files/<{filename}>"
    response = requests.get(url)
    content = response.json()['content']
    try:
        with open(filename, "wb") as f:
            f.write(content)
    except FileExistsError:
        logger.exception("File already exists.")
        raise


def list_dir():
    url = f"{LOCAL_HOST}/files/list"
    return requests.get(url)


def get_file_metadata(filename: str):
    url = f"{LOCAL_HOST}/files/<{filename}>"
    response = requests.get(url)
    return response.json()


def change_password(username: str, password: str) -> requests.Response:
    url = f"{LOCAL_HOST}/user"
    payload = {'username': username, 'password': password}
    response = requests.put(url, json=payload)
    return response.json()


def read_jwt_token():
    with open(TOKEN_FILE_PATH, "r") as f:
        token = f.read()
    return token


def write_jwt_token(token):
    with open(TOKEN_FILE_PATH, "w") as f:
        f.write(token)


