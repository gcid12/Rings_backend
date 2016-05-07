#!/bin/bash
#virtualenv --no-site-packages --distribute env && source env/bin/activate && pip install -r requirements.txt

#This should be in the cloudformation template and it is for the APP not for the server

echo 'Installing dependencies...'

sudo yum install gcc-c++
sudo yum install openssl-devel


pwd
cd /var/www/app
pwd
virtualenv --no-site-packages --distribute env && source env/bin/activate
pip install flask
pip install flask-login
pip install flask-openid
pip install flask-bcrypt
pip install tornado
pip install requests
pip install couchdb
pip install elasticsearch
pip install elasticsearch_dsl
#pip install -U cchardet
pip install flanker
pip install Wand
pip install boto
pip install supervisor

echo 'Setting up supervisord'

#Prepare supervisor config
echo_supervisord_conf > /tmp/supervisord.ini
echo '[include]' >> /tmp/supervisord.ini
echo 'files = /etc/supervisord.d/*.ini' >> /tmp/supervisord.ini
sudo cp /tmp/supervisord.ini /etc/supervisord.ini

echo 'Installing Avispa configuration'

aws s3 cp s3://myring-infra/avispa/20160501/env_config.py env_config.py
id

echo 'Creating avispa log folder'

sudo mkdir -m 755 -p /var/www/log/avispa
sudo chown -R ec2-user /var/www/log
