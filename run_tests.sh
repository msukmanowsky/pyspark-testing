#!/usr/bin/env bash
python setup.py clean bdist_egg
nosetests "$@"
