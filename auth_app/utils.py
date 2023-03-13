import random
import hashlib

from config.config_parser import config


def generate_salt():
    """Generates a random salt string for password."""
    salt = ''.join(random.choice(config()['UTILS']['characters_for_salt']) for _ in range(random.randint(8, 16)))
    return salt


def hash_sha256_password(password):
    """Hashes the password with SHA256."""
    hash_obj = hashlib.sha256()
    hash_obj.update(password.encode('utf-8'))
    salt = generate_salt()
    hash_obj.update(salt.encode('utf-8'))
    hash_obj.update(config()["AUTH"]["secret_key"].encode('utf-8'))
    return f"{hash_obj.hexdigest()}{salt}"
