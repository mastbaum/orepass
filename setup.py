import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "orepass",
    version = "0.5",
    author = "Andy Mastbaum",
    author_email = "amastbaum@gmail.com",
    description = ("Middleware adding document-level user authentication to CouchDB"),
    license = "BSD",
    keywords = "couchdb wsgi middleware security document authentication",
    url = "http://github.com/mastbaum/orepass",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "License :: OSI Approved :: BSD License",
    ],

    packages=['orepass', 'orepass.core', 'orepass.handlers'],
    scripts=['bin/orepass.wsgi'],
)

