#!/bin/bash

export FLASK_APP=app.py
flask db migrate
flask db upgrade
