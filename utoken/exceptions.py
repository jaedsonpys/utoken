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

class Base(Exception):
    pass


class InvalidKeyError(Base):
    def __init__(self):
        super().__init__('Chave inválida.')


class InvalidContentTokenError(Base):
    def __init__(self):
        super().__init__('Conteúdo do token é inválido.')


class InvalidTokenError(Base):
    def __init__(self):
        super().__init__('Token inválido.')


class ExpiredTokenError(Base):
    def __init__(self):
        super().__init__('O token foi expirado.')


if __name__ == '__main__':
    raise InvalidKeyError
