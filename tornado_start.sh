#!/bin/bash

#killall python
#deactivate
#source env/bin/activate
#nohup python tornado_start.py &

#sudo service nginx restart

#Stop server
source life/server_stop.sh
#Stop application
source life/app_stop.sh
#Start application
source life/app_start.sh
#Start server
source life/server_start.sh

