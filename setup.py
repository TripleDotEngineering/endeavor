#!/usr/bin/env python
################################################################################
#
# setup.py
#
# Copyright (c) 2021, Triple Dot Engineering LLC
#
# This file defines the package installation.
#
################################################################################
import setuptools

with open('./README.md') as fh:
    long_description = fh.read()

with open('./requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='endeavor',
    version='0.1.0',
    description='Endeavor Architecture Framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Triple Dot Engineering',
    author_email='',
    url='https://triple.engineering',
    packages=[
        'endeavor'
    ],
    package_dir={"": "src"},
    package_data={"endeavor": ["templates/*"]},
    entry_points = {
        'console_scripts': [
            'evdoc = endeavor.evdoc:main',
        ],
    },
    license="MIT",
    install_requires=requirements,
    python_requires=">=3.6"
)
