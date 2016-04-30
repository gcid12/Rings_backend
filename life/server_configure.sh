#!/bin/bash

chkconfig nginx on
rm /etc/nginx/nginx.conf
ln -s /var/www/app/tornado_nginx.conf /etc/nginx/nginx.conf
sudo service nginx restart