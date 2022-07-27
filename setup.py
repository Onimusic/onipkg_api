from distutils.core import setup
from setuptools import find_packages
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    # Project name:
    name='oni_api_helper',
    # Packages to include in the distribution:
    packages=['oni_api_helper', *find_packages(',')],
    # Project version number:
    version='1.0',
    # List a license for the project, eg. MIT License
    license='',
    # Short description of your library:
    description='Helper para consumo de APIs',
    # Long description of your library:
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Your name:
    author='Lucas Heilbuth Nazareth de Sousa',
    # Your email address:
    author_email='lucasheilbuth@yahoo.com.br',
    # Link to your github repository or website:
    url='https://github.com/LucasHeilbuth',
    # Download Link from where the project can be downloaded from:
    download_url='https://github.com/Onimusic/oni_api_helper.git',
    # List of keywords:
    keywords=['onimusic'],
    # List project dependencies:
    install_requires=[
        'requests',
    ],
    # https://pypi.org/classifiers/
    classifiers=["Private :: Do Not Upload"]
)