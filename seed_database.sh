#!/bin/bash

rm db.sqlite3
rm -rf ./HecatesHearthapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations HecatesHearthapi
python3 manage.py migrate HecatesHearthapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

