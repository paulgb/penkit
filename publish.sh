#!/bin/sh

python setup.py sdist
twine upload dist/*

