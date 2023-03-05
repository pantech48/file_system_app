"""Main module for working with file_storage."""
import argparse

from file_system.file_service import FileSystem
from file_system import utils


parser = argparse.ArgumentParser(description='App for working with file_storage.')
parser.add_argument('--create', default='', help='Creates a file with given data. Default data - empty string.')
parser.add_argument('--delete', help='Deletes file with given path.')
parser.add_argument('--read', help='Reads content of given file.')
parser.add_argument('--metadata', help="Returns file's metadata.")

args = parser.parse_args()


if __name__ == "__main__":
    if args.create:
        FileSystem.create_file(args.create)
    elif args.delete:
        FileSystem.delete_file(args.delete)
    elif args.read:
        FileSystem.read_file(args.read)
    elif args.metadata:
        utils.metadata_str(FileSystem.get_metadata(args.metadata))
