#!/usr/bin/env bash

ln -sf "$PWD"/awp/__main__.py /usr/local/bin/alfred-workflow-packager
ln -sf "$PWD"/awp/__main__.py /usr/local/bin/workflow-packager
/usr/local/bin/pip2 install biplist jsonschema
