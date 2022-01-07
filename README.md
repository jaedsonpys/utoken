# UToken - Tokens seguros.
![BADGE](https://img.shields.io/static/v1?label=status&message=em%20desenvolvimento&color=green)
![BADGE](https://img.shields.io/static/v1?label=language&message=python&color=blue)

UToken (ou Unhandleable Token) é uma bilioteca criada para ser
utilizada na geração de tokens seguros e íntegros, ou seja, não
podem ser alterados. Veja o que você pode fazer com o UToken:

- Criar tokens seguros
- Inserir um conteúdo no token
- Definir tempo de expiração para o token


## Atalhos

- [Como usar](#Como-usar)
  - [Criando um token](#Criando-um-token)
  - [Decodificando um token](#Decodificando-um-token)
  - [Tratando exceções](#Tratando-exceções)

# Como usar

Aqui vai um breve tutorial sobre como utilizar o UToken de forma simples.

## Criando um token

Vamos começar criando um token, veja o código abaixo:

```python
from utoken import encode

# definindo nossa chave
KEY = 'secret-key'

# codificando
my_token = encode({'message': 'Firlast'}, KEY)
print(my_token)

# > eyJtZXNzYWdlIjogIkZpcmxhc3QifQ.5c99ae8e7ce3a000d5b0c35cb53e9e8f
```

Primeiro passamos como parâmetro para utoken.encode() o conteúdo do token, que pode ser um dicionário ou lista, depois,
passamos a chave que vai ser utilizada para codificar. Após isso, temos o nosso token.

A chave que foi usada para codificar o token, também será usada para decodificá-lo.

## Decodificando um token

Agora, vamos decodificar um token. Veja o código abaixo:

```python
from utoken import decode

# definindo nossa chave
KEY = 'secret-key'
token = 'eyJtZXNz...'

# decodificando
my_decode_token = decode(token, KEY)
print(my_decode_token)

# > {'message': 'Firlast'}
```

Pronto! Nosso token foi decodificado. em utoken.decode() passamos como parâmetro o token e a chave utilizada na codificação, simples.
