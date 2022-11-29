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

from . import exceptions


def _has_valid_key(payload: str, key: str, proof_hash: str) -> bool:
    joined_data = str(payload + key).encode()
    hash_check = md5(joined_data).hexdigest()
    return hash_check == proof_hash


def _payload_is_expired(payload: dict):
    max_age = payload.get('max-time')
    if max_age:
        max_age_date = datetime.strptime(max_age, '%Y-%m-%d %H-%M-%S')
        return datetime.now() > max_age_date


def encode(payload: dict, key: str) -> str:
    """Create a new UToken.

    By adding the `max-time` key and placing a
    `datetime.timedelta` object in its payload, you
    define the maximum token lifetime, after which the
    decoding attempt will throw an exception.

    :param payload: The token payload
    :type payload: dict
    :param key: Secret key for token encoding
    :type key: str
    :return: Returns the token in string format
    :rtype: str
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


def decode(utoken: str, key: str) -> dict:
    """Decode the UToken and returns its payload.

    :param utoken: Encoded UToken
    :type utoken: str
    :param key: Key used for token encoding
    :type key: str
    :raises exceptions.InvalidTokenError: Raise if token is invalid
    :raises exceptions.InvalidKeyError: Raise if key is invalid
    :raises exceptions.InvalidContentTokenError: Raise if content is invalid
    :raises exceptions.ExpiredTokenError: Raise if token has expired
    :return: Return token payload
    :rtype: dict
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

    payload_expired = _payload_is_expired(payload_json)

    if payload_expired:
        raise exceptions.ExpiredTokenError('The token has reached the expiration limit')
    elif payload_expired is False:
        payload_json.pop('max-time')

    return payload_json


def decode_without_key(token: str) -> dict:
    """Decodes the token without performing an
    integrity check, i.e. no secret key is needed.

    :param token: Token
    :type token: str
    :raises InvalidTokenError: Invalid Token
    :raises InvalidContentTokenError: Invalid content
    :raises ExpiredTokenError: Expired Token
    :return: Returns the content of the token
    :rtype: dict
    """

    token_parts = token.split('.')

    if len(token_parts) != 2:
        raise exceptions.InvalidTokenError('Token is invalid')

    payload, proof_hash = token_parts
    payload_b64 = str(payload + '==').encode()
    decoded_payload = urlsafe_b64decode(payload_b64).decode()

    try:
        payload_json: dict = json.loads(decoded_payload)
    except json.JSONDecodeError:
        raise exceptions.InvalidContentTokenError('Token payload is not convertible to JSON')

    payload_expired = _payload_is_expired(payload_json)

    if payload_expired:
        raise exceptions.ExpiredTokenError('The token has reached the expiration limit')
    elif payload_expired is False:
        payload_json.pop('max-time')

    return payload_json
