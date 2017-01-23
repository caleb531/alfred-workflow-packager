#!/usr/bin/env python
# coding=utf-8

from setuptools import setup


# Get long description (used on PyPI project page)
def get_long_description():
    try:
        # Use pandoc to create reStructuredText README if possible
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except:
        return None


setup(
    name='alfred-workflow-packager',
    version='1.2.0',
    description='A CLI utility for packaging and exporting Alfred workflows',
    long_description=get_long_description(),
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
        'biplist >= 1, < 2',
        'jsonschema >= 2, < 3'
    ],
    entry_points={
        'console_scripts': [
            'awp=awp.main:main'
        ]
    }
)
