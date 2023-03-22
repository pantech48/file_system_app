""" Module with request functions """
import requests
import sys
import os

sys.path.append(r"C:\\Users\\YPutrin\\Course_007\\file_system_app")

from config.config_parser import config
from logs.logger import logger


LOCAL_HOST = config()["ROUTES"]["local_host"]
TOKEN_FILE_PATH = config()["CLIENT"]["home_directory"]
TOKEN_HEADER = config()["AUTH"]["jwt_token_header"]


def sign_up(username: str, password: str, email: str) -> dict:
    url = f"{LOCAL_HOST}/user"
    payload = {
        'username': username,
        'password': password,
        'email': email,
        }
    response = requests.post(url, json=payload)
    return response.json()


def sign_in(username: str, password: str) -> dict:
    url = f"{LOCAL_HOST}/login"
    response = requests.get(url, auth=(username, password))
    return response.json()['token']


def upload_file(filename: str, token: str = None) -> dict:
    try:
        with open(filename, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        logger.exception("File not found.")
        raise
    url = f"{LOCAL_HOST}/files"
    payload = {
        'content': content,
        }
    response = requests.post(url, json=payload, headers=jwt_token_header(token))
    return response.json()


def download_file(filename: str, token: str = None) -> None:
    url = f"{LOCAL_HOST}/files/<{filename}>"
    response = requests.get(url, headers=jwt_token_header(token))
    content = response.json()['content']
    try:
        with open(filename, "wb") as f:
            f.write(content)
    except FileExistsError:
        logger.exception("File already exists.")
        raise


def list_dir(token: str = None) -> dict:
    url = f"{LOCAL_HOST}/files/list"
    response = requests.get(url, headers=jwt_token_header(token))
    return response.json()


def get_file_metadata(filename: str, token: str = None) -> dict:
    url = f"{LOCAL_HOST}/files/<{filename}>"
    response = requests.get(url, headers=jwt_token_header(token)).json()
    metadata = response['metadata']
    return metadata


def change_password(username: str, password: str) -> dict:
    url = f"{LOCAL_HOST}/user"
    payload = {
        'username': username,
        'password': password,
        }
    response = requests.put(url, json=payload)
    return response.json()


def jwt_token_header(token: str = None) -> dict:
    return {TOKEN_HEADER: token}


def prepare_transaction_for_uploading(path: str) -> dict:
    """Prepare transaction for uploading a file."""
    url = f"{LOCAL_HOST}/files/transaction"
    payload = {
        'path': path,
        'size': os.path.getsize(path),
        }
    response = requests.post(url, json=payload)
    return response.json()
