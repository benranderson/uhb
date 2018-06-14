#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import uhb

from setuptools import setup, find_packages


setup(
    name="uhb",
    version=uhb.__version__,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ben Randerson",
    author_email="ben.m.randerson@gmail.com",
    url="https://github.com/benranderson/uhb",
    packages=find_packages(include=["uhb"]),
    entry_points={"console_scripts": ["uhb=uhb.cli:main"]},
    install_requires=open("requirements.txt").readlines(),
    include_package_data=True,
    license="MIT License",
    zip_safe=False,
    keywords="upheaval buckling uhb engineering pipelines",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Other Audience",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
