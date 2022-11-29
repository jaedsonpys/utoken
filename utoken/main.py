# UToken
# Copyright (C) 2022  Jaedson Silva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime
from hashlib import md5
from typing import Union

from . import exceptions


def _has_valid_key(payload: str, key: str, proof_hash: str) -> bool:
    joined_data = str(payload + key).encode()
    hash_check = md5(joined_data).hexdigest()
    return hash_check == proof_hash


def encode(payload: dict, key: str) -> str:
    """Create a new token Token.

    :param content: Payload of the token.
    :param key: Key for encoding.
    :return: Returns the token.
    """

    max_time: datetime = payload.get('max-time')

    if max_time:
        payload['max-time'] = max_time.strftime('%Y-%m-%d %H-%M-%S')

    payload_json = json.dumps(payload).encode()

    payload_b64 = urlsafe_b64encode(payload_json).decode()
    payload_b64 = payload_b64.replace('=', '')

    joined_data = str(payload_b64 + key).encode()
    finally_hash = md5(joined_data).hexdigest()
    utoken = '.'.join([payload_b64, finally_hash])

    return utoken


def decode(utoken: str, key: str) -> Union[dict, list]:
    """Decode the UToken
    and returns its contents.

    :param utoken: Token UToken.
    :param key: Key used in encoding.
    :return: Returns the content of the token
    """

    token_parts = utoken.split('.')

    if len(token_parts) != 2:
        raise exceptions.InvalidTokenError('Token is invalid')
    else:
        payload, proof_hash = token_parts
        if not _has_valid_key(payload, key, proof_hash):
            raise exceptions.InvalidKeyError('The key provided is invalid')

    payload_b64 = str(payload + '==').encode()
    decoded_payload = urlsafe_b64decode(payload_b64).decode()

    try:
        payload_json: dict = json.loads(decoded_payload)
    except json.JSONDecodeError:
        raise exceptions.InvalidContentTokenError('Token payload is not convertible to JSON')

    max_age = payload_json.get('max-time')

    if max_age:
        payload_json.pop('max-time')
        max_age_date = datetime.strptime(max_age, '%Y-%m-%d %H-%M-%S')

        if datetime.now() > max_age_date:
            raise exceptions.ExpiredTokenError('The token has reached the expiration limit')

    return payload_json


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
        raise exceptions.InvalidTokenError('Token is invalid')

    content, hash = token_parts
    base64_content = str(content + '==').encode()
    decode_content = urlsafe_b64decode(base64_content).decode()

    try:
        content_json: dict = json.loads(decode_content)
    except json.JSONDecodeError:
        raise exceptions.InvalidContentTokenError('Token content is invalid')

    max_age = content_json.get('max-time')

    if max_age:
        content_json.pop('max-time')
        max_age_date = datetime.strptime(max_age, '%Y-%m-%d %H-%M-%S')

        if datetime.now() > max_age_date:
            raise exceptions.ExpiredTokenError('The token has reached the expiration limit')

    return content_json
