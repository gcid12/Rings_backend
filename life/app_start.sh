#!/bin/bash

pwd
cd /var/www/app
pwd
echo $PATH
source env/bin/activate
echo $PATH
#nohup python /var/www/app/tornado_start.py &
python /var/www/app/tornado_start.py &