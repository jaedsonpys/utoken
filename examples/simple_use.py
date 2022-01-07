from utoken import encode, decode
from os import urandom

KEY = urandom(64).hex()
my_token = encode({'name': 'Jaedson'}, KEY)
my_decoded_token = decode(my_token, KEY)

print(my_token)
print(my_decoded_token)
