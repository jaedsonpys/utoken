# UToken - Secure tokens.

![BADGE](https://img.shields.io/static/v1?label=language&message=python&color=blue)

UToken (or Unhandleable Token) is a library created to be
used in the generation of safe and sound tokens, that is, not
can be changed. Here's what you can do with UToken:

- Create secure tokens
- Insert a content in the token
- Set expiration time for token


## Shortcuts

- [UToken - Secure tokens.](#utoken---secure-tokens)
  - [Shortcuts](#shortcuts)
- [Installation](#installation)
- [How to use](#how-to-use)
  - [Creating a token](#creating-a-token)
  - [Decoding a token](#decoding-a-token)
- [License](#license)

# Installation

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
my_token = encode({'message': 'Firlast'}, KEY)
print(my_token)

# > eyJtZXNzYWdlIjogIkZpcmxhc3QifQ.5c99ae8e7ce3a000d5b0c35cb53e9e8f
```

First we pass as a parameter to `utoken.encode()` the content of the token, which can be a dictionary or list, then
we pass the key that will be used to encrypt. After that, we have our token.

We can also add the token expiration time using the `max-time` key in our `dictionary`, see:

```python
from utoken import encode
from datetime import datetime, timedelta

max_time = datetime.now() + timedelta(minutes=5)

# encoding
my_token = encode({'message': 'Firlast', 'max-time': max_time}, 'KEY')
```

After the maximum time is reached, the `ExpiredTokenError` exception will be thrown.

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

# > {'message': 'Firlast'}
```

Ready! Our token has been decoded. In `utoken.decode()` we pass as a parameter the token and the key used in the encoding, simple.

If you set an expiration time on the token, you will get an **exception when trying** to decode the token if the token is expired, for that,
do an exception handling:

```python
from utoken import decode
from utoken import ExpiredTokenError

# defining our key
KEY = 'secret-key'
token = 'eyJtZXNz...'

# decoding
try:
    my_decode_token = decode(token, KEY)
except ExpiredTokenError:
    print('Token has expired')
else:
    print(my_decode_token)
```

# License

    GNU GENERAL PUBLIC LICENSE
    Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.