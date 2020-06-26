#!/bin/sh

. venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=./english_speak_backend/kernel.py
python -m flask run --host=0.0.0.0  -p 5000
