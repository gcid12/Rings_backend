#!/bin/bash

echo "Removing past supervisor config..."
rm -rf /etc/supervisor.d/flask.ini
rm -rf /etc/rc.d/init.d/supervisord
rm -rf /etc/supervisord.conf