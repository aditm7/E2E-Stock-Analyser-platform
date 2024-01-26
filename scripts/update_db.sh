#!/bin/bash

export FLASK_APP=main.py
flask db migrate
flask db upgrade
