#!/bin/bash
sudo apt-get update
sudo apt-get -y install python3-pip python3-dev libmysqlclient-dev libpq-dev
sudo pip3 install -r requirements.txt
sudo apt-get -y install apache2
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo rm /etc/apache2/sites-enabled/*
sudo cp servicio.conf /etc/apache2/sites-enabled
python3 secret.py >> ~/.bashrc
echo "export DJANGO_SETTINGS_MODULE='Gaude.production'" >> ~/.bashrc
