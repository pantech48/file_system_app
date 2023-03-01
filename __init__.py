import hashlib
import base64
import os

content = 'asda'

signature = 'asda'

file_hash = hashlib.sha256(content.encode()).digest()
signature = base64.b64decode(signature)
print(file_hash, "|", signature)