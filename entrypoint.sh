#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata apps/accounts/fixtures/user.json
python manage.py loaddata apps/demand/fixtures/uf_cities.json
exec "$@"