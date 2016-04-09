#!/bin/bash

killall python
deactivate
source env/bin/activate
nohup python tornado_start.py &

sudo service nginx restart
