#!/bin/bash

echo 'Starting supervisor...'
service supervisord start

#supervisorctl reload
#service supervisord start
#pwd
#cd /var/www/app
#pwd
#echo $PATH
#source env/bin/activate
#echo $PATH
#nohup python /var/www/app/tornado_start.py &
#echo "Starting app.."
#result="$(nohup python /var/www/app/tornado_start.py &)"
#echo "App Started"