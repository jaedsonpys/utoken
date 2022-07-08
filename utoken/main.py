import json
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime
from hashlib import md5
from typing import Union

from . import exceptions


def encode(content: dict, key: str) -> str:
    """Create a new token Token.

    :param content: Content of the token.
    :param key: Key for encoding.
    :return: Returns the token.
    """

    max_time: datetime = content.get('max-time')

    if max_time:
        content['max-time'] = max_time.strftime('%Y-%m-%d %H-%M-%S')

    content_json_bytes = json.dumps(content).encode()

    content_base64 = urlsafe_b64encode(content_json_bytes).decode()
    content_base64 = content_base64.replace('=', '')

    # Hash of: content_base64 + key
    join_key = str(content_base64 + key).encode()
    finally_hash = md5(join_key).hexdigest()

    # finally token
    utoken = '.'.join([content_base64, finally_hash])

    return utoken


def decode(utoken: str, key: str) -> Union[dict, list]:
    """Decode the UToken
    and returns its contents.

    :param utoken: Token UToken.
    :param key: Key used in encoding.
    :return: Returns the content of the token
    """

    split_token = utoken.split('.')

    try:
        _content, _hash = split_token
    except ValueError:
        raise exceptions.InvalidTokenError

    _join_key = str(_content + key).encode()
    _hash_content = md5(_join_key).hexdigest()

    if _hash_content == _hash:
        _base64_content = str(_content + '==').encode()
        _decode_content = urlsafe_b64decode(_base64_content).decode()

        # convert content to dict or list
        try:
            _content_json: dict = json.loads(_decode_content)
        except json.JSONDecodeError:
            raise exceptions.InvalidContentTokenError
        else:
            max_age = _content_json.get('max-time')

            if max_age:
                _content_json.pop('max-time')
                max_age_date = datetime.strptime(max_age, '%Y-%m-%d %H-%M-%S')

                if datetime.now() > max_age_date:
                    raise exceptions.ExpiredTokenError

            return _content_json

    raise exceptions.InvalidKeyError


def decode_without_key(token: str) -> dict:
    """Decode the UToken
    and returns its contents without
    need the key.

    This decoding does not guarantee
    that the token is healthy.

    :param token: Token
    :type token: str
    :raises InvalidTokenError: Invalid Token
    :raises InvalidContentTokenError: Invalid content
    :raises ExpiredTokenError: Expired Token
    :return: Returns the content of the token
    :rtype: dict
    """

    token_parts = token.split('.')

    if len(token_parts) < 2 or len(token_parts) > 2:
        raise exceptions.InvalidTokenError

    _content, _hash = token_parts
    _base64_content = str(_content + '==').encode()
    _decode_content = urlsafe_b64decode(_base64_content).decode()

    try:
        _content_json: dict = json.loads(_decode_content)
    except json.JSONDecodeError:
        raise exceptions.InvalidContentTokenError
    else:
        max_age = _content_json.get('max-time')

        if max_age:
            _content_json.pop('max-time')
            max_age_date = datetime.strptime(max_age, '%Y-%m-%d %H-%M-%S')

            if datetime.now() > max_age_date:
                raise exceptions.ExpiredTokenError

    return _content_json
