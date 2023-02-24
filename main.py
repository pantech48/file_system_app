import argparse
import file_service


parser = argparse.ArgumentParser(description='App for working with files.')
parser.add_argument('create')
parser.add_argument('-delete')
parser.add_argument('-read')

args = parser.parse_args()


if __name__ == "__main":
    ...