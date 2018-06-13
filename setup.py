#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import uhb

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["click"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    name="uhb",
    version=uhb.__version__,
    description="Upheaval Buckling Tools",
    long_description=readme,
    author="Ben Randerson",
    author_email="ben.m.randerson@gmail.com",
    url="https://github.com/benranderson/uhb",
    packages=find_packages(include=["uhb"]),
    entry_points={"console_scripts": ["uhb=uhb.cli:main"]},
    include_package_data=True,
    install_requires=requirements,
    license="MIT License",
    zip_safe=False,
    keywords="upheaval buckling uhb engineering pipelines",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Other Audience",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
