#!/bin/bash

echo 'Installing dependencies...'

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
pip install dnsq
pip install algoliasearch

#DEV ONLY
pip install flask_debugtoolbar


#echo 'Installing Avispa configuration'
#aws s3 cp s3://myring-infra/avispa/20160730/env_config.py env_config.py

echo 'Creating avispa log folder'

sudo mkdir -p log/avispa

