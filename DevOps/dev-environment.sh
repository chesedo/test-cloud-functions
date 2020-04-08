#!/bin/bash

# Install Python 3.7
apt install -y python3.7 python3.7-distutils python3.7-venv

# Install Poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python