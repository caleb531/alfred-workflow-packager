#!/usr/bin/env python
# coding=utf-8

import json
import os
import os.path

import jsonschema


# Validate the given utility configuration JSON against the schema
def validate_config(config):

    schema_path = os.path.join(
        os.path.dirname(__file__), 'data', 'config-schema.json')
    with open(schema_path, 'r') as schema_file:
        jsonschema.validate(config, json.load(schema_file))
