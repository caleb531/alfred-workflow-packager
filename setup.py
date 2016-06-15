#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(
    name='alfred-workflow-packager',
    version='0.10.0',
    description='A CLI utility for packaging and exporting Alfred workflows',
    url='https://github.com/caleb531/alfred-workflow-packager',
    author='Caleb Evans',
    author_email='caleb@calebevans.me',
    license='MIT',
    keywords='alfred workflow package export',
    packages=['alfred_workflow_packager'],
    package_data={
        'alfred_workflow_packager': ['data/config-schema.json']
    },
    install_requires=[
        'biplist >= 1, < 2',
        'jsonschema >= 2, < 3'
    ],
    entry_points={
        'console_scripts': [
            'alfred-workflow-packager=alfred_workflow_packager.main:main',
            'workflow-packager=alfred_workflow_packager.main:main'
        ]
    }
)
