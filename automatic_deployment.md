##Automatic Deployment

####Cloud Formation:
```
yum -y install nginx
```

####Code Deploy:

Before placing code

```
mkdir /var/www/app
chkconfig nginx on
ln -s /etc/nginx/nginx.conf /var/www/app/tornado_nginx.conf
```

#After placing code
```
virtualenv --no-site-packages --distribute env && source env/bin/activate && pip install -r requirements.txt
source var/www/app/tornado_start.sh
```
