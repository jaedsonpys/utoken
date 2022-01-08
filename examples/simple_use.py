from utoken import encode, decode
from os import urandom

KEY = 'secret-key'
my_token = encode({'message': 'Firlast'}, KEY)
my_decoded_token = decode(my_token, KEY)

print(my_token)
print(my_decoded_token)
