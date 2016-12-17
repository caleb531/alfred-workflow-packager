#!/usr/bin/env python
# coding=utf-8

import argparse
import json

import awp.packager
import awp.validator


# Parse arguments given via command-line interface
def parse_cli_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--validate', action='store_true',
        help='validates the utility configuration file for this project')
    parser.add_argument(
        '--export', '-e', nargs='?', const='', default=None,
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

    if cli_args.validate:
        awp.validator.validate_config(config)
    else:
        awp.packager.package_workflow(
            config,
            version=cli_args.version,
            export_file=cli_args.export)


if __name__ == '__main__':
    main()
