#!/usr/bin/env bash
python setup.py clean
python setup.py sdist
nosetests "$@"
