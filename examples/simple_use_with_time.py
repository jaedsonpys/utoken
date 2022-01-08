from utoken import encode, decode
from utoken import ExpiredTokenError

from datetime import datetime
from datetime import timedelta

from time import sleep

KEY = 'secret-key'

# Em max_time definimos que o token expira
# daqui a 5 segundos.

max_time = datetime.now() + timedelta(seconds=5)
my_token = encode({'message': 'Firlast', 'max-time': max_time}, KEY)

print(my_token)
sleep(6)

try:
    my_decoded_token = decode(my_token, KEY)
except ExpiredTokenError:
    print('O token está expirado.')
else:
    print(f'Conteúdo do token: {my_decoded_token}')
