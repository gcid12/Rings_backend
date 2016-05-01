#!/bin/bash
#virtualenv --no-site-packages --distribute env && source env/bin/activate && pip install -r requirements.txt
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

aws s3 cp s3://myring-infra/avispa/20160501/env_config.py env_config.py
id
mkdir -m 755 -p /var/www/log/avispa
