import random
from config_parser import config


# todo: move in config file symbols var
def generate_filename():
    symbols = config()["ascii_and_digits"]
    filename = ''.join(random.choice(symbols) for _ in range(10))
    return filename


def metadata_str(metadata):
    for field, data in metadata.items():
        print(field, ": ", data)
