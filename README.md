# UToken - Secure tokens

UToken (or Unhandleable Token) is a library designed to generate secure tokens with a guarantee of integrity for any type of project. With this project you can add payload and token lifetime.

To install UToken, use the `pip` package manager:

```
pip install utokeniz
```

# How to use

Here's a short tutorial on how to use UToken in a simple way.

## Creating a token

Let's start by creating a token, see the code below:

```python
from utoken import encode

# defining our key
KEY = 'secret-key'

# encoding
my_token = encode({'message': 'Hello World!'}, KEY)
print(my_token)
```

First we pass as a parameter to `utoken.encode()` the payload of the token, which must be a dictionary, then we pass the key that will be used to encode the token. After that we have our token in a string returned by the function.

### Define expiration time

We can also add the token **expiration time** using the `max-time` switch in our `dict`, after the maximum time is reached the `ExpiredTokenError` exception will be thrown:

```python
from utoken import encode
from datetime import datetime, timedelta

max_time = datetime.now() + timedelta(minutes=5)
my_token = encode({'message': 'Hello!', 'max-time': max_time}, 'secret-key')
```

## Decoding a token

Now, let's decode a token. See the code below:

```python
from utoken import decode

# defining our key
KEY = 'secret-key'
token = 'eyJtZXNz...'

# decoding
my_decode_token = decode(token, KEY)
print(my_decode_token)
```

Ready! Our token has been decoded. In `utoken.decode()` we pass as a parameter the token and the key used in the encoding, simple.

# License

```
Copyright © 2023 Jaedson Silva
BSD-3-Clause License
```

This project uses the `BSD-3-Clause` license. Please [see the license file](https://github.com/jaedsonpys/utoken/blob/master/LICENSE) to more informations.