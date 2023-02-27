import random

from config_parser import config


def generate_filename():
    symbols = config()["characters_for_generate_filename_function"]
    filename = ''.join(random.choice(symbols) for _ in range(config()["length_of_filename"]))
    return filename


def metadata_str(metadata):
    for field, data in metadata.items():
        print(field, ": ", data)
