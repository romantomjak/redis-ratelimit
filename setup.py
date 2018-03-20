# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    with open(path.join(here, 'README'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name='redis-ratelimit',
    version='1.0.0',
    description='A fixed window rate limiting based on Redis',
    long_description=long_description,
    url='https://github.com/r00m/redis-ratelimit',
    author='Roman Tomjak',
    author_email='r.tomjaks@gmail.com',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='redis rate-limit ratelimit',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['redis'],
)
