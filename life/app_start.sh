#!/bin/bash

pwd
echo $PATH
source env/bin/activate
echo $PATH
nohup python /var/www/app/tornado_start.py &