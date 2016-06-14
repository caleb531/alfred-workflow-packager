#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(
    name='alfred-workflow-packager',
    version='0.9',
    description='A CLI utility for packaging and exporting Alfred workflows',
    url='https://github.com/caleb531/alfred-workflow-packager',
    author='Caleb Evans',
    author_email='caleb@calebevans.me',
    license='MIT',
    keywords='alfred workflow package export',
    packages=['awp'],
    install_requires=[
        'biplist >= 1, < 2',
        'jsonschema >= 2, < 3'
    ],
    entry_points={
        'console_scripts': [
            'alfred-workflow-packager=awp.packager:main',
            'workflow-packager=awp.packager:main'
        ]
    }
)
