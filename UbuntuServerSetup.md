#Ubuntu Virtual Server Setup for Avispa

Create an instance with any of the following operating system:
```
Ubuntu14.04-64 Minimal for VSI  , Ubuntu14.10-64
```

This instance should be already connected to the internet. The Hosting provider should give you the Public IP address at least a set of credentials to access. Most probably it will be 'root'. 

Access the instance from your Terminal. Provide given password when asked for it

```
# ssh <user>@<public_ip_address>
```

It is a realy good idea to change the password immediatelly after you use access.

```
passwd <user> 
```


###Installations

Before we start lets update our local update package
```
# apt-get update
```

#####VIM

Install vim (Sysadmins will always need it)
```
# apt-get install vim
```
#####Nginx

Now we install the web server Nginx
```
# apt-get install nginx
```

####uWSGI
Install uWSGI
```
# apt-get install uwsgi
```

```
# apt-get install build-essential python python-dev
```

```
# apt-get install uwsgi-plugin-python
```

```
# apt-get install python-pip
```

```
# pip install uwsgi
```

####Python Dev
```
# apt-get install python-dev
```

#####CouchDB
Install CouchDB
```
$ apt-get install couchdb
```


##### Imagemagick + Wand
```
apt-get install libmagickwand-dev
```

##### Virtualenv

Install the virtualenv package:
```
$ apt-get install python-virtualenv
```

##### Git

Install GIT package:
```
# apt-get install git
```

##### Htpasswd
Install the Apache2-utils package:
```
apt-get install apache2-utils
```

If you are running Ubuntu from a Virtual Server, run the following:
```
$ sudo dpkg-divert --local --rename --add /sbin/initctl
$ ln -s /bin/true /sbin/initctl
```
Original Reference: https://www.nesono.com/node/368

### Verifying installations

Check that the web-server has been installed correctly. Just type the public ip address in your browser. You should be greeted by Nginx with a meesage like this:

```
Welcome to nginx!
If you see this page, the nginx web server is successfully installed and working. Further configuration is required.
```

### Configuring CouchDB

Open your /etc/couchdb/local.ini file and uncomment and change the line 'bind_address' to: 
```
bind_address = 0.0.0.0
```

Save that file and run
```
$ couchdb
```

It should greet you with this message:
```
Apache CouchDB is running as process xxxx, time to relax.
```

If it shows you this error:
```
Failure to start Mochiweb: eaddrinuse
```

CouchDB might be already running. Do:
```
$ netstat -tlpn
```
Find the process that is using the port 5984
```
tcp        0      0 127.0.0.1:5984          0.0.0.0:*               LISTEN      <####>/beam 
```
And kill it
```
$ kill <####>
```

This will have CouchDB aquire the new configuration. Check it is running using your browser
```
http://<public-ip-address>:5984
```
It should show you a Json message like this:
 ```
 {"couchdb":"Welcome","uuid":"e9efe39bfe10462ab812509e6f27c91e","version":"1.6.0","vendor":{"name":"Ubuntu","version":"14.10"}}
 ```

There are two more things we need to do with CouchDB. First run in your browser:
```
http://<public-ip-address>:5984/_utils/verify_install.html
```
And click on "Verify your installation" It should respond: "Your installation looks fine. Time to Relax."

Now assign  CouchDB robot-user. Go to:
```
http://<public-ip-address>/_utils
```
You'll see in the lower-right corner a message like : 'Welcome to Admin Party, fix this' . Click on it and a pop-up window will appear asking you for a username and a password. Assign them. You'll use them later in this configuration as *couch-db_admin-robot-user* and *couch-db-password-for-robot-user*



### Cloning Avispa Source Code


Create the directories where the application is going to live
```
$ mkdir /var/www
$ mkdir /var/www/avispa
$ mkdir /var/www/_images
```



Change the ownership to the group that will have access to it
```
chown -R :www-data /var/www/avispa
```

We'll use the Machine-User method to connect to GitHub where each machine has its own set of credentials to access the Private Github repository. For that we need to create the SSH keys for the server and give the Public Key to GitHub.

First check if there are any SSH Keys in that server already
```
$ ls -al ~/.ssh
```
Look for files name 'id_rsa.pub' or 'id_dsa.pub'. Since this is a new server there should not be any. 

Generate a new SSH Key
```
$ ssh-keygen -t rsa -C "RobotUser_<public_ip_address>"
```

Then add your new key to the ssh-agent:
```
$ eval "$(ssh-agent -s)"
$ ssh-add ~/.ssh/id_rsa
```

Please note that everytime you spawn any ssh -> git activity you'll have to be logged in as the current user

You need to copy exactly as it is (no extra blankspaces) the contents of ~/.ssh/id_rsa.pub into your clipboard
You'll paste them in Github

Run this command and copy from your terminal using Command+c
```
cat  ~/.ssh/id_rsa.pub
```

Run the following command to paste the public key into your clipboard (or copy it manually)
$ pbcopy < ~/.ssh/id_rsa.pub

####Add your SSH key to GitHub

Log in to GitHub with you personal account. You need to have access to the private Repository

1. In the user bar in the top-right corner of any page click on the settings icon (a small gear)
2. Click 'SSH Keys' in the left sidebar
3. Click 'Add SSH Key'
4. In the Title field, write "RobotUser-<public-ip-address>"
5. Paste the ssh key into the "Key" field
6. Click 'Add key'

Please notice that this procedure will change greatly in the following subversions as RobotUsers will have their own GITHUB accounts. 


#### Clone the Private Repository

If everything was setup correctly you should be able to clone the Repository without a problem
```
$ git clone git@github.com:MyRing/avispa.git /var/www/avispa
```


Create and activate a virtual environment, and install Flask into it:
```
$ cd /var/www/avispa
$ virtualenv --no-site-packages --distribute venv && source venv/bin/activate && pip install -r requirements.txt
```

You'll have to test if all the modules where installed correctly. Run this for complete list:
```
$ cat requirements.txt
```
And this
```
$ pip freeze
```
For what what installed. Verify that all the items in requirements.txt show in pip freeze. If they don't you'll have to manually install what is missing
```
pip install <missing-module>
```

To check the installation run installation_test.py :

```
# python installation_test.py
```

And enter the following address in your browser:
```
http://<public_ip_address>:8080
```
You should see a "Flask Installation successful" message.  


####Initializing Avispa's Flask App Databases.


Rename env_config.py.template to env_config.py .

```
cp env_config.py.template env_config.py
```

Assign the values for this machine
```
IMAGE_STORE = '/var/www/_images'
IMAGE_CDN_ROOT = ''
STATIC_CDN_ROOT = ''

COUCHDB_USER = u''
COUCHDB_PASS = u''
COUCHDB_SERVER = ""

SMTPSERVER = u''
SMTPPORT = 587
FROMEMAIL = u''
FROMPASS = u''

PREVIEW_LAYER = 2
```

Assign the PythonPath running this command. This will be in the initialization script but we are manually testing flask right now
```
$ export PYTHONPATH=${PYTHONPATH}:/var/www/avispa/
```


As a test to see if all the dependencies for Flask are ready, run
```
python /var/www/avispa/run.py
```

It will show you the login screen. Run this to install the initial DBs

```
http://<public_ip_address>:8080/_tools/install
```

Stop the Flask server with CTRL+C



#### Configuring Nginx

Create the symbolic link that will point the config files to this project 
```
ln -s /var/www/avispa app
```

Remove Nginx's default site configuration
```
# rm /etc/nginx/sites-enabled/default
```

Symlink nginx.conf to nginx's configuration directory and restart nginx
```
# ln -s /var/www/app/nginx.conf /etc/nginx/conf.d/
```
IMPORTANT: Check that there is no other file in /etc/nginx/conf.d . That would cause a "502 Bad Gateway" error

If the Nginx config file uses SSL certificates you need to place them in their place. Usually it is in /etc/ssl . Assuming that those certificates already exist in another server you just need to copy them here:

```
scp root@<origin-ip-address>:/etc/ssl/nameofcertificate.key /etc/ssl
scp root@<origin-ip-address>:/etc/ssl/public.crt /etc/ssl
```

Now restart the server 
```
# /etc/init.d/nginx restart
```

And go to the following address in your browser
```
http://<public_ip_address>
```

It should return a 502 Bad Gateway error. Not bad, this means Nginx is already using nginx.conf
The problem is that uwsgi.sock doesn't exist yet. Create this file if it doesn't exist.
```
vim /var/www/app/uwsgi.ini
```

Write the following in the file:
```
# uwsgi.ini

[uwsgi]
#application's base folder
base = /var/www/app

#python module to import
app = run
module = %(app)

home = %(base)/venv
pythonpath = %(base)

#socket file's location
socket = /var/www/app/%n.sock

#permissions for the socket file
chmod-socket    = 644

#the variable that holds a flask application inside the module imported at line #6
callable = app

#location of log files
logto = /var/log/uwsgi/%n.log
```

Now create a new directory for uwsgi log files
```
mkdir -p /var/log/uwsgi
```
And make it available to the deployment team
```
chown -R :deployteam /var/log/uwsgi
```



Execute uWSGI and pass it the newly created configuration file
```
uwsgi --ini /var/www/app/uwsgi.ini --chown-socket=www-data:www-data
```
The Terminal will stay idle. That is ok. It means it is serving pages.
That is ok but if you close that terminal window the process will stop. 
We will use uWSGI Emperor to run uWSGI as a background service.




Now try to reach the server using the browser. Use https:// as otherwise it will redirect you to other server
```
https://<this-machine-ip-address>
```
Please note it will warn you about unsecure certificates. What happens is that the SSL certificate expects the domain it was issued for. Just say yes and add the exception.

By now you should be able to see the web application in the browser.

Troubleshooting: 
1. If the browser can't find the website it is an Nginx issue. Check the Nginx log
2. It the browser shows a 501 error it is a uWSGI issue. Check the uWSGI log


##### uWSGI Emperor

uWSGI Emperor is responsible for reading config files and spawning uWSGI processes to execute them.

Create a new upstart configuration file to execute emperor

```
vim /etc/init/uwsgi.conf
```
And write the following in the file:
```
description "uWSGI"
start on runlevel [2345]
stop on runlevel [06]
respawn

env UWSGI=/var/www/app/venv/bin/uwsgi
env LOGTO=/var/log/uwsgi/emperor.log
env MYRING_CSRF_SESSION_KEY='<unique-key>'

exec $UWSGI --master --emperor /etc/uwsgi/vassals --die-on-term --uid www-data --gid www-data --logto $LOGTO
```


This script will look for the config files in /etc/uwsgi/vassals folder. Create it and symlink it
```
 mkdir /etc/uwsgi
 mkdir /etc/uwsgi/vassals
 ln -s /var/www/app/uwsgi.ini /etc/uwsgi/vassals
```

Also, the last line states that the user that will be used to execute the daemon is 'www-data'.
For simplicity's sake, let's set him as the owner of the application and log folders
```
 chown -R www-data:www-data /var/www/app/
 chown -R www-data:www-data /var/www/_images/
 chown -R www-data:www-data /var/log/uwsgi/
```

Since both, nginx and uWSGI, are now being run by the same user, we can make a security improvement to our uWSGI configuration. Open up the uwsgi config file (/var/www/app/uwsgi.ini) and change the value of chmod-socket from 666 to 644:
```
...
#permissions for the socket file
chmod-socket = 644
```

Create the start/reset file
```
vim /var/www/avispa/start.sh
```

Paste the following in the file
```
/etc/init.d/nginx stop
couchdb -k
deactivate
source /var/www/avispa/venv/bin/activate
stop uwsgi
export PYTHONPATH=${PYTHONPATH}:/var/www/avispa/
/etc/init.d/nginx start
couchdb -b
start uwsgi
```

Now we can start the uWSGI job
```
# source /var/www/avispa/start.sh
```

One more thing. Since it is not good to have access to the database via a public address. Open /etc/couchdb/local.ini file and comment out the line 'bind_address' : 
```
#bind_address = <public-ip-address>
```


####Troubleshooting

If something goes wrong, the first place to check is the log files. 

#####CouchDB
```
tail /var/log/couchdb/couch.log
```

#####Nginx 

http access logs 
```
tail /var/log/nginx/access.log
```
http error logs 
```
tail /var/log/nginx/error.log
```

Nginx status
```
systemctl status nginx.service
```

#####Emperor

To see if the uWSGI process was spawned correctly
```
tail /var/log/uwsgi/emperor.log
```

If the emperor seems to be not working when you call start uwsgi run this:
```
/var/www/app/venv/bin/uwsgi --master --emperor /etc/uwsgi/vassals --die-on-term --uid www-data --gid www-data --logto /var/log/uwsgi/emperor.log

```
Now try to access via browser. If you see the page the problem is not emperor o uWSGI but the 'start' command


#####uWSGI
To see the all the dynamic content activity including the python print() and python error traces
```
tail /var/log/uwsgi/uwsgi.log
```



#### Static Files

Add the following rule to serve the Static files from avispa
```
location /static {
    root /var/www/app/;
}
```
As a result, all static files located at /var/www/app/static will be served by Nginx.

#### Sometimes you need to turn on and off a service:

Virtual Environment
```
$ deactivate
$ source /var/www/app/venv/bin/activate
```

Couchdb
```
$ couchdb -k
$ couchdb -b
```
Nginx 
```
$ /etc/init.d/nginx stop
$ /etc/init.d/nginx start
```

uWSGI
```
$ stop  uwsgi
$ start uwsgi
```

#### Hard Restarting the Machine
In case you need to restart the server you'll have to restart the virtual environment and all the services. Run the following commands:
```
$ source /var/www/app/venv/bin/activate
$ couchdb -b
$ /etc/init.d/nginx start
$ start uwsgi 
```













