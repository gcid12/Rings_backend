
##Installing CouchDB 1.5.1 on Amazon Linux AMI 2014.03.1
29 April 2014

source http://www.everyhaironyourhead.com/installing-couchdb-1-5-1-on-amazon-linux-ami-2014-03-1/


This article is a follow up to my previous article Installing CouchDB 1.5 on Amazon Linux found here.

####Core deps and dev tools.

    Enable the EPEL Repo by editing the file /etc/yum.repos.d/epel.repo and setting it to enabled.

    Next install the deps and tools.

    sudo yum install gcc gcc-c++ libtool libicu-devel openssl-devel autoconf-archive erlang python27 python-sphinx help2man

####Get the SpiderMonkey JS Engine and build it.
'''
wget http://ftp.mozilla.org/pub/mozilla.org/js/js185-1.0.0.tar.gz
tar xvfz js185-1.0.0.tar.gz
cd js-1.8.5/js/src
./configure
make
sudo make install
'''
You should see it installed under /usr/local/lib

####Build CouchDB.

    Download the source package for CouchDB, unpack it and cd in.

    Point it to the required libs and configure.
'''
    ./configure --with-erlang=/usr/lib64/erlang/usr/include --with-js-lib=/usr/local/lib/ --with-js-include=/usr/local/include/js/

    make
    sudo make install
'''
####Prepare the CouchDB installation.

    Make a couchdb user.
'''
    sudo useradd -r -d /usr/local/var/lib/couchdb -M -s /bin/bash couchdb
'''
    Set the file ownerships.
'''
    sudo chown -R couchdb:couchdb /usr/local/etc/couchdb
    sudo chown -R couchdb:couchdb /usr/local/var/lib/couchdb
    sudo chown -R couchdb:couchdb /usr/local/var/log/couchdb
    sudo chown -R couchdb:couchdb /usr/local/var/run/couchdb
    sudo chmod 0775 /usr/local/etc/couchdb
    sudo chmod 0775 /usr/local/var/lib/couchdb
    sudo chmod 0775 /usr/local/var/log/couchdb
    sudo chmod 0775 /usr/local/var/run/couchdb
'''
####Prepare the init scripts.

    Link the init script and copy the log rotate script to /etc.
'''
    sudo cp /usr/local/etc/logrotate.d/couchdb /etc/logrotate.d
    sudo ln -s /usr/local/etc/rc.d/couchdb /etc/init.d/couchdb
'''
    This and most other linux distros don’t include /usr/local/lib in ld, so CouchDB will have problems finding the SpiderMonkey libs we installed there earlier. One way to solve this is to add the following line to the top of the /etc/init.d/couchdb startup script.
'''
    export LD_LIBRARY_PATH=/usr/local/lib
'''
    See man page for ldconfig for more info and tweet back with a better solution.

    You may want to edit /usr/local/etc/default/couchdb to turn off the auto respawn.

    To get it to autostart, just use the standard linux setup tools for running service scripts.
'''
    sudo chkconfig --add couchdb
'''
    It should pick up the default run levels needed from the script, but in case it doesn’t, you can do it manually like this...
'''
    sudo chkconfig --level 3 couchdb on
    sudo chkconfig --level 4 couchdb on
    sudo chkconfig --level 5 couchdb on
'''
    You can sudo chkconfig —list to confirm its there. See man chkconfig for more details.

####Relax.

Finally reboot (or just start couchdb from the script) and confirm its running with curl http://127.0.0.1:5984/
