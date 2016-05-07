#!/bin/bash

echo "Removing past supervisor config..."
rm -rf /etc/supervisor.d
rm -rf /etc/rc.d/init.d/supervisord