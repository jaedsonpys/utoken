from hashlib import md5
import json
from base64 import urlsafe_b64encode
from base64 import urlsafe_b64decode


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
    join_key = (content_base64 + key).encode()
    finally_hash = md5(join_key).hexdigest()

    # finally token
    utoken = '.'.join([content_base64, finally_hash])

    return utoken


if __name__ == '__main__':
    from os import urandom

    KEY = urandom(64).hex()
    encode({'name': 'Jaedson'}, KEY)
