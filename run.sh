#!/usr/bin/env bash

cd "$(dirname "$0")"

python manage.py makemigrations

python manage.py runserver

