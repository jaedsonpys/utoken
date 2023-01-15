from time import sleep
from datetime import timedelta

import utoken

KEY = 'secret-key'

# In "expires_in" we set token timeout of 5 seconds
my_token = utoken.encode({'name': 'Maria'}, KEY, expires_in=timedelta(seconds=5))
print(my_token)

sleep(6)

try:
    payload = utoken.decode(my_token, KEY)
except utoken.exceptions.ExpiredTokenError:
    print('O token está expirado.')
else:
    print(f'Conteúdo do token: {payload}')
