import random
import string


# todo: move in config file symbols var
def generate_filename():
    symbols = f"{string.ascii_lowercase}{string.digits}"
    filename = ''.join(random.choice(symbols) for _ in range(10))
    return filename

