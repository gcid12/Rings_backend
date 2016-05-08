#!/bin/bash

echo "Killing supervisord..."
sudo service supervisord stop
echo "Killing application (if any left)..."
killall -q python
echo "Kill Done"
#deactivate