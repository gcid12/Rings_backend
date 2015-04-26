/etc/init.d/nginx stop
couchdb -k
deactivate
source /var/www/app/venv/bin/activate
stop uwsgi
export PYTHONPATH=${PYTHONPATH}:/var/app/myring/
/etc/init.d/nginx start
couchdb -b
start uwsgi
