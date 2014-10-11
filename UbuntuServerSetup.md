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

Install vim (Sysadmins will always need it)
```
# apt-get install vim
```

Now we install the web server Nginx
```
# apt-get install nginx
```

Check that the web-server has been installed correctly. Just type the <public_ip_address> in your browser. YOu should be greeted by Nginx with a meesage like this:

```
Welcome to nginx!
If you see this page, the nginx web server is successfully installed and working. Further configuration is required.
```

Now, create the directories where the application is going to live
```
mkdir /var/www
mkdir /var/www/myring
```

Change the ownership to the group that will have access to it
```
chown -R :deployteam /var/www/myring 
```

Install the virtualenv package:
```
# apt-get install python-virtualenv
```

Create and activate a virtual environment, and install Flask into it:
```
# cd /var/www/myring
# virtualenv venv
# . venv/bin/activate
# pip install flask
```

To check for installation create hello.py file:
```
# vim hello.py
```

Press 'i' and start writing the following code:
```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

```
To save press "ESC" key and type ":wq" then ENTER

Now execute hello.py
```
# python hello.py
```

And enter the following address in your browser:
```
http://<public_ip_address>:8080
```

You should see a "Hello World" message






Then GIT

```
# apt-get install git
```







