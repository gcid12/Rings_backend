#!/bin/bash

chkconfig nginx on
rm /etc/nginx/nginx.conf
ln -s /var/www/app/nginx_tornado.conf /etc/nginx/nginx.conf