#!/bin/bash

export FLASK_APP=solar-rest-fake.py
export FLASK_DEBUG=True
flask run --host=0.0.0.0
