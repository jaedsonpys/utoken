import json
import datetime
from hashlib import md5
from base64 import urlsafe_b64decode, urlsafe_b64encode

from . import exceptions


def _has_valid_key(payload: str, key: str, proof_hash: str) -> bool:
    joined_data = str(payload + key).encode()
    hash_check = md5(joined_data).hexdigest()
    return hash_check == proof_hash


def _payload_is_expired(payload: dict):
    max_age = payload.get('exp')
    if max_age:
        max_age_date = datetime.datetime.strptime(max_age, '%Y-%m-%d %H-%M-%S')
        return datetime.datetime.now() > max_age_date


def encode(payload: dict, key: str, expires_in: datetime.timedelta = None) -> str:
    """Creates a new UToken token.

    If you pass a `datetime.timedelta` type object
    to the `expires_in` argument, you will define the
    maximum time of the token. If the token expires
    and you try to decode it, the `ExpiredTokenError`
    exception will be thrown.

    :param payload: Data to be encoded
    :type payload: dict
    :param key: Key to encode
    :type key: str
    :param expires_in: Token expiration time, defaults to None
    :type expires_in: datetime.timedelta, optional
    :return: Returns the encoded token
    :rtype: str
    """

    if expires_in:
        exp: datetime.datetime = datetime.datetime.now() + expires_in
        payload['exp'] = exp.strftime('%Y-%m-%d %H-%M-%S')

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
