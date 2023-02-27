import argparse
import file_service
import utils


parser = argparse.ArgumentParser(description='App for working with files.')
parser.add_argument('--create', default='', help='Creates a file with given data. Default data - empty string.')
parser.add_argument('--delete', help='Deletes file with given path.')
parser.add_argument('--read', help='Reads content of given file.')
parser.add_argument('--metadata', help="Returns file's metadata.")

args = parser.parse_args()


if __name__ == "__main__":
    if args.create:
        file_service.create_file(args.create)
    elif args.delete:
        file_service.delete_file(args.delete)
    elif args.read:
        file_service.read_file(args.read)
    elif args.metadata:
        utils.metadata_str(file_service.get_metadata(args.metadata))
