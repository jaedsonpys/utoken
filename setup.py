from setuptools import setup
from utoken import __version__

setup(
    name='utokeniz',
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    description='Create healthy and secure authentication tokens with UTokeniz.',
    version=__version__,
    packages=['utoken'],
    url='https://github.com/jaedsonpys/utoken',
    project_urls={
        'Source code': 'https://github.com/jaedsonpys/utoken'
    },
    license='GPL'
)