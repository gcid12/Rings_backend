MyRing Development Environment  0.1
======
MAJOR = 0
MINOR = 1

###Preparing your Development Machine (OSX).

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

### Creating the MyRing Environment 

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


###Installing stuff in the MyRing Environment 

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

### Cloning source code from the Insect Mothership

There will be as many repositories as projects (insects). The reason for doing this instead of having a huge "include all" repository, is that every insect has to be able to run independently. The insects will communicate between them via public APIs and should not share anything (config files, databases, etc). However there will be a common server environment on top of which stable versions will run (myring.<MAJOR>.<MINOR>[.<MICRO>]). This way we can replace an insect in the future for another version without having to worry about strange dependencies. Also, there will be different versions that use different technologies.

In order to start interacting with GITHUB you need to generate your SSH Keys and add them to your GITHUB Personal Account.

Please follow the instructions here:

https://help.github.com/articles/generating-ssh-keys

Once done you just need to clone the Repository. In your command line type

```
$ cd ~/Code
$ git clone <SSH_CLONE_URL_OF_THE_INSECT_YOU_ARE_CLONING>
```

### Installing Avispa App Database

#### CouchDB

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

### Image upload storage and serving

#### Imagemagick and Wand

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





