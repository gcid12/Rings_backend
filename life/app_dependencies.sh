#!/bin/bash
#virtualenv --no-site-packages --distribute env && source env/bin/activate && pip install -r requirements.txt

virtualenv --no-site-packages --distribute env && source env/bin/activate
pip install flask
pip install flask-login
pip install flask-openid
pip install flask-bcrypt