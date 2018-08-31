#!/bin/bash

export FLASK_APP=solar_rest_origin_fake.py
export FLASK_DEBUG=True
flask run --host=0.0.0.0
