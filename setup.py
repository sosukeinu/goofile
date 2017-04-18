try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

config = {
    'name': 'goofile',
    'description': 'Update of https://code.google.com/archive/p/goofile/ for Python 3',
    'author': 'Jonathan Batteas <jonathanbatteas@gmail.com>',
    'url': '',
    'download_url': '',
    'author_email': 'jonathanbatteas@gmail.com',
    'version': '1.6',
    'install_requires': required,
    'packages': [],
    'scripts': ['goofile.py'],
    'entry_points': {
        'console_scripts': [
            'goofile = goofile:main',
        ]
    }

}

setup(**config)