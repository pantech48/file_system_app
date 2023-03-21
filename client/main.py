import requests
import threading
from getpass import getpass

from client_requests import (
    sign_up,
    sign_in,
    change_password,
    list_dir,
    upload_file,
    download_file,
    get_file_metadata
)
from logs.logger import logger

JWT_TOKEN = None


def main_menu() -> None:
    """Main menu table of contents."""
    logger.info("Main menu")
    logger.info("1. Sign up")
    logger.info("2. Sign in")
    logger.info("3. Change password")
    logger.info("4. Upload file")
    logger.info("5. Download file")
    logger.info("6. List dir")
    logger.info("7. Get file metadata")
    logger.info("8. Quit")


def sign_up_flow() -> None:
    """Flow for signing up."""
    username = input("Enter a username: ")
    password = getpass("Enter a password: ")
    email = input("Enter an email: ")
    result = sign_up(username, password, email)
    logger.info(result)


def sign_in_flow() -> None:
    """Flow for signing in."""
    global JWT_TOKEN
    username = input("Enter a username: ")
    password = getpass("Enter a password: ")
    result = sign_in(username, password)
    JWT_TOKEN = result
    logger.info(result)


def change_password_flow() -> None:
    """Flow for changing password."""
    username = input("Enter a username: ")
    password = getpass("Enter a new password: ")
    result = change_password(username, password)
    logger.info(result)


def upload_file_flow() -> None:
    """Flow for uploading a file."""
    filename = input("Enter the file path: ")

    def target():
        try:
            result = upload_file(filename, token=JWT_TOKEN)
            logger.info(result)
        except FileNotFoundError:
            logger.exception("File not found.")

    thread = threading.Thread(target=target)
    thread.start()
    thread.join()


def download_file_flow() -> None:
    """Flow for downloading a file."""
    filename = input("Enter the file name to download: ")

    def target():
        try:
            download_file(filename, token=JWT_TOKEN)
            logger.info("File downloaded.")
        except FileExistsError:
            logger.exception("File already exists.")

    thread = threading.Thread(target=target)
    thread.start()
    thread.join()


def list_dir_flow() -> None:
    """Flow for listing directory."""
    result = list_dir(token=JWT_TOKEN)
    logger.info(f"Files in the directory: {result['files']}")


def get_file_metadata_flow() -> None:
    """Flow for getting file metadata."""
    filename = input("Enter the file name: ")
    metadata = get_file_metadata(filename, token=JWT_TOKEN)
    logger.info(f"File metadata: {metadata}")


def main() -> None:
    """Main function."""
    while True:
        try:
            main_menu()
            choice = int(input("Enter your choice: "))
            if choice == 1:
                sign_up_flow()
            elif choice == 2:
                sign_in_flow()
            elif choice == 3:
                change_password_flow()
            elif choice == 4:
                upload_file_flow()
            elif choice == 5:
                download_file_flow()
            elif choice == 6:
                list_dir_flow()
            elif choice == 7:
                get_file_metadata_flow()
            elif choice == 8:
                break
            else:
                logger.info("Invalid choice.")
        except KeyboardInterrupt:
            logger.info("Exiting...")
            break


if __name__ == "__main__":
    main()
