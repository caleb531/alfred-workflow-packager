#!/usr/bin/env python3
# coding=utf-8

from setuptools import setup


# Get long description (used on PyPI project page)
def get_long_description():
    with open('README.md', 'r') as readme_file:
        return readme_file.read()


setup(
    name='alfred-workflow-packager',
    version='1.2.1',
    description='A CLI utility for packaging and exporting Alfred workflows',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/caleb531/alfred-workflow-packager',
    author='Caleb Evans',
    author_email='caleb@calebevans.me',
    license='MIT',
    keywords='alfred workflow package export',
    packages=['awp'],
    package_data={
        'awp': ['data/config-schema.json']
    },
    install_requires=[
        'jsonschema >= 4, < 5'
    ],
    entry_points={
        'console_scripts': [
            'awp=awp.main:main'
        ]
    }
)
