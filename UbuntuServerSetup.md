#Ubuntu Virtual Server Setup for MyRing

Create an instance with the following operating system:
```
Ubuntu14.04-64 Minimal for VSI
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

Check that the web-server has been installed correctly. Just type the <public_ip_address> in your browser. YOu should be greeted by Nginx with a meesage like this:

```
Welcome to nginx!
If you see this page, the nginx web server is successfully installed and working. Further configuration is required.
```

#####CouchDB
Install CouchDB
```
$ apt-get install couchdb
```

Open your /etc/couchdb/local.ini file and uncomment and change the line 'bind_address' to: 
```
bind_address = <public-ip-address>
```

Save that file and run
```
$ couchdb
```

It should greet you with this message:
```
Apache CouchDB has started. Time to relax.
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



### Cloning MyRing Source Code


Create the directories where the application is going to live
```
$ mkdir /var/www
$ mkdir /var/www/myring
```

Change the ownership to the group that will have access to it
```
chown -R :deployteam /var/www/myring 
```

We'll use the Machine-User method to connect to GitHub where each machine has its own set of credentials to access the Private Github repository. For that we need to create the SSH keys for the server and give the Public Key to GitHub.

First check if there is any SSH Keys in that server already
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
$ git clone git@github.com:MyRing/avispa.git /var/www/myring
```


Create and activate a virtual environment, and install Flask into it:
```
$ cd /var/www/myring
$ virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt
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
You should see a "Flask Installation successful" message. CTR+C in the terminal otherwise it will keep running. 

Now it is time to test myring
```
$ python run.py
```

Reload your browser:
```
http://<public_ip_address>:8080
```




### uWSGI

We need uWSGI to server dynamic content in production. 

Install the compilers and tools first

```
# apt-get install build-essential python python-dev
```

Now install uWSGI
```
# pip install uwsgi
```

#### Configuring Nginx

Remove Nginx's default site configuration
```
# rm /etc/nginx/sites-enabled/default
```

Create a new configuration file for MyRing application
```
vim /var/www/myring/myring_nginx.conf
```
And put this inside:
```
server {
    listen      80;
    server_name localhost;
    charset     utf-8;
    client_max_body_size 75M;

    location / { try_files $uri @yourapplication; }
    location @yourapplication {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/myring/myring_uwsgi.sock;
    }
}
```

Symlink the new file to nginx's configuration directory and restart nginx
```
# ln -s /var/www/myring/myring_nginx.conf /etc/nginx/conf.d/
```

Now restart the server 
```
# /etc/init.d/nginx restart
```

And go to the following address in your browser
```
http://<public_ip_address>
```

It should return a 502 Bad Gateway error.Not bad, this means Nginx is already using myring_nginx.conf
The problem is that myring_uwsgi.sock doesn't exist yet. Let's create it
```
vim /var/www/myring/myring_uwsgi.ini
```

Write this in the file:
```
[uwsgi]
#application's base folder
base = /var/www/myring

#python module to import
app = hello
module = %(app)

home = %(base)/venv
pythonpath = %(base)

#socket file's location
socket = /var/www/myring/%n.sock

#permissions for the socket file
chmod-socket    = 666

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
uwsgi --ini /var/www/myring/myring_uwsgi.ini
```
The Terminal will stay idle. That is ok. It means it is serving pages.
That is ok but if you close that terminal window the process will stop. 
We will use uWSGI Emperor to run uWSGI as a background service.

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

env UWSGI=/var/www/myring/venv/bin/uwsgi
env LOGTO=/var/log/uwsgi/emperor.log

exec $UWSGI --master --emperor /etc/uwsgi/vassals --die-on-term --uid www-data --gid www-data --logto $LOGTO

```

This script will look for the config files in /etc/uwsgi/vassals folder. Create it and symlink it
```
# mkdir /etc/uwsgi
# mkdir /etc/uwsgi/vassals
# ln -s /var/www/myring/myring_uwsgi.ini /etc/uwsgi/vassals
```

Also, the last line states that the user that will be used to execute the daemon is 'www-data'.
For simplicity's sake, let's set him as the owner of the application and log folders
```
# chown -R www-data:www-data /var/www/myring/
# chown -R www-data:www-data /var/log/uwsgi/
```

Since both, nginx and uWSGI, are now being run by the same user, we can make a security improvement to our uWSGI configuration. Open up the uwsgi config file (myring_uwsgi.ini) and change the value of chmod-socket from 666 to 644:
```
...
#permissions for the socket file
chmod-socket = 644
```

Now we can start the uWSGI job
```
# start uwsgi
```

####Troubleshooting

If something goes wrong, the first place to check is the log files. By default, nginx writes error message to the file /var/log/nginx/errors.log.

We’ve configured uWSGI emperor to write it’s logs to /var/log/uwsgi/emperor.log. Also this folder contains separate log files for each configured application. In our case - /var/log/uwsgi/demoapp_uwsgi.log.

#### Static Files

Add the following rule to serve the Static files from myring
```
location /static {
    root /var/www/myring/;
}
```
As a result, all static files located at /var/www/myring/static will be served by Nginx.











