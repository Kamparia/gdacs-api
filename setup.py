#!/usr/bin/env python3

from setuptools import setup, find_packages

version = "0.1"

setup(
    name="gdacs-api",
    version=version,
    author="Olaoye Anthony Somide",
    author_email="olaoye.somide@wfp.org",
    license="Apache 2.0",
    url="https://github.com/Kamparia/gdacs-api",
    download_url=(
        f'https://github.com/Kamparia/gdacs-api/archive/{version}.tar.gz'
    ),
    description="Unofficial python library for working with GDACS API.",
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=["*test*"]),    
    include_package_data=True,
    install_requires=[
        "requests",
        "xmltodict",
        "cachetools",
    ],
    keywords='gdacs disasters earthquakes tropical-cyclones floods',
    python_requires=">=3.5",    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)