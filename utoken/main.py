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

    join_key = str(content_base64 + key).encode()
    finally_hash = md5(join_key).hexdigest()

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
        content, hash = split_token
    except ValueError:
        raise exceptions.InvalidTokenError

    join_key = str(content + key).encode()
    hashcontent = md5(join_key).hexdigest()

    if hashcontent != hash:
        raise exceptions.InvalidKeyError

    base64_content = str(content + '==').encode()
    decode_content = urlsafe_b64decode(base64_content).decode()

    try:
        content_json: dict = json.loads(decode_content)
    except json.JSONDecodeError:
        raise exceptions.InvalidContentTokenError

    max_age = content_json.get('max-time')

    if max_age:
        content_json.pop('max-time')
        max_age_date = datetime.strptime(max_age, '%Y-%m-%d %H-%M-%S')

        if datetime.now() > max_age_date:
            raise exceptions.ExpiredTokenError

    return content_json


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

    content, hash = token_parts
    base64_content = str(content + '==').encode()
    decode_content = urlsafe_b64decode(base64_content).decode()

    try:
        content_json: dict = json.loads(decode_content)
    except json.JSONDecodeError:
        raise exceptions.InvalidContentTokenError

    max_age = content_json.get('max-time')

    if max_age:
        content_json.pop('max-time')
        max_age_date = datetime.strptime(max_age, '%Y-%m-%d %H-%M-%S')

        if datetime.now() > max_age_date:
            raise exceptions.ExpiredTokenError

    return content_json
