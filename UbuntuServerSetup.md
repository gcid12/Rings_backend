#Ubuntu Virtual Server Setup for MyRing

Create an instance with the following operating system:
```
Ubuntu14.04-64 Minimal for VSI
```

You'll have to enter as Root and create the users from there. Softlayer doesn't do it from their "Passwords" interface.

###Installations

Before we start lets update our local update package
```
sudo apt-get update
```

Start with VIM

```
$ apt-get install vim
```

Then GIT

```
$ apt-get install git
```

Check what version of Python is installed by default
```
$ python
```
It will return something like this:
```
Python 2.7.6 (default, Mar 22 2014, 22:59:56) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
```

If it shows Python 3.x you'll have to change the default to be 2.7.x 
Please look in the internet for instructions on how to do this.

Now install pip
```
apt-get install python-pip
```






