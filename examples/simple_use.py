import utoken

KEY = 'secret-key'
my_token = utoken.encode({'message': 'Firlast'}, KEY)
payload = utoken.decode(my_token, KEY)

print(my_token)
print(payload)
