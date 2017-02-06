avispa
======

Tool to manually capture data into a local ring


"get_a" = Show all the rings of user <a>
"get_a_b" = Show all the items of ring <a>/<b>
"get_a_b_c" = Show item <a>/<b>/<c>
"get_a_x" = Show all collections from user <a>
"get_a_x_y" = Show collection <y> from user <a>
"get_a_x_y_b" = Show ring <a>/<b> as part of collection <y>
"get_a_x_y_b_c" = Show item <a>/<b>/<c> as part of collection <y>
"post_a" = Create new ring for user <a>
"post_a_b" = Create new item in ring <a>/<b>
"post_a_x" = Create new collection for user <a>
"put_a" = Update user <a>
"put_a_b" = Update ring <a>/<b>
"put_a_b_c" = Update item <a>/<b>/<c>
"put_a_x_y" = Update collection <y> from user <a>
"delete_a" = Delete user <a>
"delete_a_b" = Delete ring <a>/<b>
"delete_a_b_c" = Delete item <a>/<b>/<c>
"delete_a_x_y" = Delete collection <y> from user <a>



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

####After placing code
```
virtualenv --no-site-packages --distribute env && source env/bin/activate && pip install -r requirements.txt
source var/www/app/tornado_start.sh
```


##Installing CouchDB 1.5.1 on Amazon Linux AMI 2014.03.1
29 April 2014

source http://www.everyhaironyourhead.com/installing-couchdb-1-5-1-on-amazon-linux-ami-2014-03-1/


This article is a follow up to my previous article Installing CouchDB 1.5 on Amazon Linux found here.

####Core deps and dev tools.

Enable the EPEL Repo by editing the file /etc/yum.repos.d/epel.repo and setting it to enabled.

Next install the deps and tools.

```
sudo yum install gcc gcc-c++ libtool libicu-devel openssl-devel autoconf-archive erlang python27 python-sphinx help2man
```

Get the SpiderMonkey JS Engine and build it.

```
wget http://ftp.mozilla.org/pub/mozilla.org/js/js185-1.0.0.tar.gz
tar xvfz js185-1.0.0.tar.gz
cd js-1.8.5/js/src
./configure
make
sudo make install
```

You should see it installed under /usr/local/lib

####Build CouchDB.

Download the source package for CouchDB, unpack it and cd in.

Point it to the required libs and configure.

```
./configure --with-erlang=/usr/lib64/erlang/usr/include --with-js-lib=/usr/local/lib/ --with-js-include=/usr/local/include/js/
make
sudo make install
```

####Prepare the CouchDB installation.
Make a couchdb user.

```
sudo useradd -r -d /usr/local/var/lib/couchdb -M -s /bin/bash couchdb
```

Set the file ownerships.

```
sudo chown -R couchdb:couchdb /usr/local/etc/couchdb
sudo chown -R couchdb:couchdb /usr/local/var/lib/couchdb
sudo chown -R couchdb:couchdb /usr/local/var/log/couchdb
sudo chown -R couchdb:couchdb /usr/local/var/run/couchdb
sudo chmod 0775 /usr/local/etc/couchdb
sudo chmod 0775 /usr/local/var/lib/couchdb
sudo chmod 0775 /usr/local/var/log/couchdb
sudo chmod 0775 /usr/local/var/run/couchdb
```

####Prepare the init scripts.

Link the init script and copy the log rotate script to /etc.

```
sudo cp /usr/local/etc/logrotate.d/couchdb /etc/logrotate.d
sudo ln -s /usr/local/etc/rc.d/couchdb /etc/init.d/couchdb
```

This and most other linux distros don’t include /usr/local/lib in ld, so CouchDB will have problems finding the SpiderMonkey libs we installed there earlier. One way to solve this is to add the following line to the top of the /etc/init.d/couchdb startup script.

```
export LD_LIBRARY_PATH=/usr/local/lib
```

See man page for ldconfig for more info and tweet back with a better solution.

You may want to edit /usr/local/etc/default/couchdb to turn off the auto respawn.

To get it to autostart, just use the standard linux setup tools for running service scripts.

```
sudo chkconfig --add couchdb
```

It should pick up the default run levels needed from the script, but in case it doesn’t, you can do it manually like this...

```
sudo chkconfig --level 3 couchdb on
sudo chkconfig --level 4 couchdb on
sudo chkconfig --level 5 couchdb on
```
You can sudo chkconfig —list to confirm its there. See man chkconfig for more details.

####Relax.

Finally reboot (or just start couchdb from the script) and confirm its running with curl http://127.0.0.1:5984/



##MyRing Development Environment  0.1
======
MAJOR = 0
MINOR = 1

####Preparing your Development Machine (OSX).

You need to do this in your development computer before starting


If you're using pip to install packages, you can get both virtualenv and virtualenvwrapper by simply installing the latter.

```
$ pip install virtualenvwrapper
```

After it's installed, add the following lines to your shell's start-up file (.zshrc, .bashrc, .profile, etc).

```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Code
source /usr/local/bin/virtualenvwrapper.sh
```

Reload your start up file (e.g. source .zshrc) and you're ready to go.  

In case you don't know where to find .bashrc , the way to find it in your mac is:

```
$ cd ~
```

This will take you to your user root, then type this:

```
$ ls -al
```

This will show you the hidden files

```

.			.Trash			.bashrc			.jjmldete		.wlkynaorc		Documents		Movies
..			.bash_history		.dropbox		.ssh			Applications		Downloads		Music
.CFUserTextEncoding	.bash_profile		.dropbox-master		.viminfo		Code			Google Drive		Pictures
.DS_Store		.bash_profile_original	.gitconfig		.virtualenvs		Desktop			Library			Public

```

If you can't find the file called .bashrc just create it using vim .bashrc   . Put this in the file:

```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Code
source /usr/local/bin/virtualenvwrapper.sh
```

I recommend you to create a folder called "Code" in your root. This is where you can put all your development.

Save the file

You'll also have to modify the file called .bash_profile for it to read .bashrc . Just type the following at the bottom of .bash_profile :

```
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
```

#### Creating the MyRing Environment 

Since all the MyRing Projects are going to be sharing the same installation it makes no sense to have a virtualenvironment for each one of them. Create just one

```
$ mkvirtualenv --no-site-packages myring_<MAJOR>.<MINOR>[.<MICRO>]
```

Where MAJOR, MINOR and MICRO are the MyRing Version you want to recreate. 

You can exit this virtual environment typying

```
$ deactivate
```

And re-activate typing

```
$ workon myring
```


####Installing stuff in the MyRing Environment 

Since you used the --no-site-packages, your virtualenv ignores anything already installed in your computer. Even if you have all the following packages installed in your computer, you'll have to install them again in the  MyRing Environment following the instructions in this document. That way we insure we all are in sync and you don't mess with other projects you are working on. In the near future there will be a module that will create automatically a precise virtualenv with the version you want to work with.

Before installing anything do

```
$workon myring_<MAJOR>.<MINOR>[.<MICRO>]
```

First we install Flask

```
pip install Flask
```

This will install Flask, Werkzeug, Jinja2, itsdangerous, and markupsafe

```
Flask==0.10.1
Jinja2==2.7.3
MarkupSafe==0.23
Werkzeug==0.9.6
itsdangerous==0.24
wsgiref==0.1.2
```

Also install py-bcrypt to hash passwords
```
pip install py-bcrypt
```


Run life dependencies shell to complete missing dependencies
```
cd life && source app_dependencies.sh
```




#### Cloning source code from the Insect Mothership

There will be as many repositories as projects (insects). The reason for doing this instead of having a huge "include all" repository, is that every insect has to be able to run independently. The insects will communicate between them via public APIs and should not share anything (config files, databases, etc). However there will be a common server environment on top of which stable versions will run (myring.<MAJOR>.<MINOR>[.<MICRO>]). This way we can replace an insect in the future for another version without having to worry about strange dependencies. Also, there will be different versions that use different technologies.

In order to start interacting with GITHUB you need to generate your SSH Keys and add them to your GITHUB Personal Account.

Please follow the instructions here:

https://help.github.com/articles/generating-ssh-keys

Once done you just need to clone the Repository. In your command line type

```
$ cd ~/Code
$ git clone <SSH_CLONE_URL_OF_THE_INSECT_YOU_ARE_CLONING>
```

#### Installing Avispa App Database

##### CouchDB

Install CouchDB in your computer

```
pip install couchdb
```

If you run 

```
pip freeze
```

You should see something like this

```
argparse==1.2.1
CouchDB==0.10
http-parser==0.8.3
restkit==4.2.2
socketpool==0.5.3
wsgiref==0.1.2
```

Start your CouchDB typing this in the command line

```
couchdb
```

You should get a similar message 

```
Apache CouchDB 1.6.0 (LogLevel=info) is starting.
Apache CouchDB has started. Time to relax.
[info] [<0.31.0>] Apache CouchDB has started on http://127.0.0.1:5984/
```

Please notice the URL. Copy and paste it in your Browser. You'll get something like this:

```
{"couchdb":"Welcome","uuid":"b4983e57a91fd84d552dd5ce86eeff6b","version":"1.6.0","vendor":{"version":"1.6.0-1","name":"Homebrew"}}
```

This means you are up and running. If this is the first time you run CouchDB in your computer, you need to Verify the installation. Go to this URL and click on "Verify your Installation"

http://127.0.0.1:5984/_utils/verify_install.html


It should return this message:

```
Your installation looks fine. Time to Relax.
```

You'll have to leave that command line open. If you close it the database will shut down (don't worry, nothing is going to be erased if you do). Of course in production this would run in the background but since you are in development you'll need this window to check how your app is interacting with COUCHDB's REST API.

#### Image upload storage and serving

##### Imagemagick and Wand

Imagemagick will process the images that are uploaded via the image widget in vespa

```
brew install imagemagick
```

Wand is the python binding for imagemagick

```
pip install wand
```

Now, create the folder that will store the images. This folder has to be outside the Avispa project. I recommend one level higher than Avispa root. The folder should be named like the handle.

```
mkdir myringimages<handle>
cd myringimages<handle>
mkdir o
mkdir r100
mkdir r240
mkdir r320
mkdir r500
mkdir r640
mkdir r800
mkdir 1024
mkdir t75
mkdir t150
```

All those folders store the different versions of the image that has been uploaded. The folder 'o' stores the original file

#### Nginx

Do it the easy way via Homebrew

```
brew install nginx
```

Open nginx.conf and change to this:

```
server {
        listen       80;
        server_name  localhost;
        root /route/to/your/image/folder/root/;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }

        location /myringimages/ {
            index index.html;
        }


```



## Avispa installation in EC2 Instance

#### Dependencies:

##### gcc
```
$ sudo yum install gcc
```

##### g++
```
sudo yum install gcc-c++
```

##### Virtualenv
```
$ sudo yum install python-virtualenv
```

##### Imagemagick + Wand
```
$ sudo yum install ImageMagick-devel
```

##### Source Code
Unzip the source code that you got from GitHub or an S3 Bucket
```
$ cd /var/www
$ unzip avispa_master.zip
```


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
$ mkdir /var/log/avispa
```



Change the ownership to the group that will have access to it
```
chown -R :www-data /var/www/avispa
chown -R www-data:www-data /var/log/avispa
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

















