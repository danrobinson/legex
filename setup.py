try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Legal citation tools.',
    'author': 'Daniel Robinson',
    'url': 'http://github.com/danrobinson/',
    'download_url': 'Where to download it.',
    'author_email': 'gottagetmac@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['legex'],
    'scripts': [],
    'name': 'legex'
}

setup(**config)