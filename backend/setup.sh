#!/bin/bash

if [ ! -d venv ]; then
    virtualenv --python=python3 venv
fi

source venv/bin/activate
pip install -r requirements.txt
