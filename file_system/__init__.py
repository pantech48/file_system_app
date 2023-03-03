import hashlib
import base64
#
# private_key = hashlib.sha256().digest()
# public_key = base64.b64encode(private_key).decode('utf-8')
# file_data = b'Hello, world!'
# file_hash = hashlib.sha256(file_data).digest()
# signature = base64.b64encode(file_hash + private_key)
# print(signature)
#
# # signature was writen to the first line of the file
# # now need to verify the file
# public_key = public_key.encode('utf-8')
# print(public_key)
# signature_from_open_file = signature
# opened_file_hash = file_hash
# computed_signature = base64.b64encode(opened_file_hash + public_key).decode('utf-8')
#
# print(computed_signature)
# print(computed_signature == signature_from_open_file.decode('utf-8'))