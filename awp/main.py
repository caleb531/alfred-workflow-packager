#!/usr/bin/env python3
# coding=utf-8

import argparse
import json

import jsonschema

import awp.packager
import awp.validator
from awp.argparse_extras import constForNargsStar


# Parse arguments given via command-line interface
def parse_cli_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='forces the copying of all files and directories')
    parser.add_argument(
        '--export', '-e',
        nargs='*',
        action=constForNargsStar,
        const=[],
        default=None,
        help='exports the installed workflow to the local project directory')
    parser.add_argument(
        '--version', '-v',
        help='the new version number to use for the workflow')
    return parser.parse_args()


# Locate and parse the configuration for the utility
def get_utility_config():
    with open('packager.json', 'r') as config_file:
        return json.load(config_file)


def main():

    cli_args = parse_cli_args()
    config = get_utility_config()

    try:
        awp.validator.validate_config(config)
        awp.packager.package_workflow(
            config,
            version=cli_args.version,
            export_files=cli_args.export,
            force=cli_args.force)
    except jsonschema.exceptions.ValidationError as error:
        print('awp (from packager.json): {}'.format(error.message))


if __name__ == '__main__':
    main()
