#!/bin/bash

chkconfig nginx on
ln -s /etc/nginx/nginx.conf /var/www/app/tornado_nginx.conf
sudo service nginx restart