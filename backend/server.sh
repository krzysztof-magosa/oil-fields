#!/bin/bash

export PYTHONPATH=$(pwd)

source venv/bin/activate
./venv/bin/python3.5 ./server.py
