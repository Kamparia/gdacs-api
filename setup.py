#!/usr/bin/env python3
import os 
import sys

from setuptools import setup

version = "2.0.0"

long_description = open('README.md').read()

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
    python_requires=">=3.6",    
    install_requires=[
        "requests>=2.10.0",
        "xmltodict",
        "cachetools",
        "pydantic",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)