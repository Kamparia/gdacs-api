#!/usr/bin/env python3
import os 
import sys
import codecs

from setuptools import setup

version = "0.1.1"

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


setup(
    name="gdacs-api",
    version=version,
    author="Olaoye Anthony Somide",
    author_email="olaoye.somide@wfp.org",
    license="MIT",
    url="https://github.com/Kamparia/gdacs-api",
    description="Unofficial python library for working with GDACS API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='gdacs disasters earthquakes tropical-cyclones earthquakes floods',
    packages=['gdacs'],
    python_requires=">=3.5",    
    install_requires=[
        "requests>=2.10.0",
        "xmltodict",
        "cachetools",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)