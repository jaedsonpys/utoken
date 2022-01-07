from hashlib import md5
import json
from base64 import urlsafe_b64encode
from base64 import urlsafe_b64decode

from exceptions import *


def encode(
        content: [dict, list],
        key: str,
) -> str:
    """Cria um novo token
    UToken.

    :param content: Conteúdo do token.
    :param key: Chave para a codificação.
    :return: Retorna o token.
    """

    content_json_bytes = json.dumps(content).encode()

    content_base64 = urlsafe_b64encode(content_json_bytes).decode()
    content_base64 = content_base64.replace('=', '')

    # Hash of: content_base64 + key
    join_key = str(content_base64 + key).encode()
    finally_hash = md5(join_key).hexdigest()

    # finally token
    utoken = '.'.join([content_base64, finally_hash])

    return utoken


def decode(
        utoken: str,
        key: str
) -> [dict, list]:
    """Decodifica o UToken
    e retorna o conteúdo dele.

    :param utoken: Token UToken.
    :param key: Chave utilizada na codificação.
    :return: Retorna o conteúdo do token
    """

    split_token = utoken.split('.')

    try:
        _content, _hash = split_token
    except ValueError:
        raise InvalidTokenError

    _join_key = str(_content + key).encode()
    _hash_content = md5(_join_key).hexdigest()

    if _hash_content == _hash:
        _base64_content = str(_content + '==').encode()
        _decode_content = urlsafe_b64decode(_base64_content).decode()

        # convert content to dict or list
        try:
            _content_json = json.loads(_decode_content)
        except json.JSONDecodeError:
            raise InvalidContentTokenError
        else:
            return _content_json

    raise InvalidKeyError


if __name__ == '__main__':
    from os import urandom

    KEY = urandom(64).hex()
    my_token = encode({'name': 'Jaedson'}, KEY)
    my_decoded_token = decode(my_token, KEY)

    print(my_token)
    print(my_decoded_token)
