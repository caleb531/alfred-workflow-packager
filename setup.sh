#!/usr/bin/env bash

/usr/local/bin/pip2 install biplist jsonschema
ln -sf "$PWD"/awp.py /usr/local/bin/alfred-workflow-packager
ln -sf "$PWD"/awp.py /usr/local/bin/workflow-packager
