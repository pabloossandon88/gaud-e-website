#!/bin/bash
source ~/.bashrc
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
sudo service apache2 restart
nohup gunicorn Gaude.wsgi:application &