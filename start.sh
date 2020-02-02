#!/usr/bin/env bash
source .venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
#export FLASK_ENV=production
export FLASK_RUN_PORT=80
flask run --host 0.0.0.0
