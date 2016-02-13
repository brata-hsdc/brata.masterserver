# Master Server for the HSDC

The Master Server is a collection of Python applications written using 
the Django framework.  The applications talk to a common database.  This
configuration uses a PostgreSQL database, although MySQL could be easily
substituted.  The applications are run in an Apache web server environment.
Some applications provide both user-facing web pages, such as a scoreboard
display for the competition, and others provide a RESTful web API for the
Raspberry Pi competition stations.

## Overview

The code is organized as a single Django project called **ms**.  Within **ms**
there are four Django apps:

* `dbkeeper` - provides Master Server database administration functions and management interface
* `scoreboard` - drives the main scoreboard or leaderboard for the competition, and possibly other status displays
* `piservice` - provides a RESTful interface for the BRATA devices and the RPi competition stations
* `teamcentral` - provides status info to competitors through a mobile device interface

## Installation

### Install and Set Up Raspbian

Download Raspbian Jessie Lite released 2015-11-21 from https://www.raspberrypi.org/downloads/raspbian/.

Unzip the zip file to get the raw SD card image. Write the raw image file to the SD card:

```sh
$ sudo dd if=2015-11-21-raspbian-jessie-lite.img of=/dev/sdX bs=4M
$ sudo sync
```

Eject SD card, insert into device, and power up.

Log-in when prompted.


TODO - config
TODO - raspi-config to expand SD card


### Update Repositories and in case remote QRCode generation goes down add QRCode generation support

```sh
# sudo apt-get update
# sudo apt-get upgrade
# sudo apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
# sudo pip install pillow
# sudo pip install qrcode
```

### Install Python

N/A Python already installed and upgraded
Ah crud need to reinstall python from source with --enabled-shared? This error came from mod_wsgi install.  Suggests there will be major performance and memory hit if not done.

### Install the Apache Web Server
```sh
# sudo apt-get install apache2
```

### Install mod_wsgi
```sh
# sudo apt-get install apache2-threaded-dev
# sudo pip install mod_wsgi
# sudo apt-get install libapache2-mod-wsgi
# sudo a2enmod wsgi <TBD is this really needed?>
```

### Install PostgreSQL
```sh
sudo apt-get install postgresql-9.1
```

### Install psycopg2
```sh
sudo apt-get install python-psycopg2
```

TODO do we need to create a virtual environment first?

### Install Django
```sh
# sudo pip install Django
```

### Install httpie

`httpie` is a command line tool that has a lot of the same functionality as `curl` and `wget`, but with
a more user-friendly command line structure, and colorful syntax highlighting.  See the
[httpie website](http://httpie.org) for more info.

`httpie` is written in Python, so it can be installed with `pip`, like this:

```sh
# sudo pip install httpie
```

## Setup

### Create the database
Create a new PostgreSQL database called `msdb`.
```sh
# cd /usr/lib/postgresql/9.1/bin
# sudo -u postgres psql
# create database msdb;
# create user pi password '<get from team>';
# grant all privileges on database msdb to pi;
# \q
```

### Clone this repository
```sh
# sudo mkdir /opt/designchallenge2016
# sudo chown pi:pi /opt/designchallenge2016
# cd /opt/designchallenge2016
# git clone https://github.com/brata-hsdc/brata.masterserver.git
```

### Modify the Apache configuration
```sh
# sudo nano /etc/apache2/sites-enabled/000-default
```
Add
```sh
WSGIScriptAlias / /opt/designchallenge2016/brata.masterserver/workspace/ms/ms/wsgi.py
WSGIPythonPath /opt/designchallenge2016/brata.masterserver/workspace/ms
<Directory /opt/designchallenge2016/brata.masterserver/workspace/ms/ms>
<Files wsgi.py>
Order deny,allow
Allow from all
</Files>
</Directory>
```

### Install the ms Django project
First change the default password from the source to match the one you set above for the pi postgres user.
```sh
# cd brata.masterserver/workspace/ms/ms
# nano settings.py
```
Find raspberry (the default pi password) and change it to your password. Save and exit the file.
Then:
```sh
# cd ..
# python manage.py migrate
```

**Note:** (JIA 12/17/2015) I had to make the following edits. FYI this was for a Debian Jessie VM running on a laptop:

   # Edit /opt/.../workspace/ms/ms/settings.py and set HOST to localhost in order to get migrate to run successfully. 
   # Edit /etc/apache2/envvars to change APACHE_RUN_USER and APACHE_RUN_GROUP from www-data to the development user; restart apache2.
   # In the /etc/apache2/sites-enabled/000-default.conf, added after "Allow from all", then restarted Apache:
   # In the /etc/apache2/sites-enabled/000-default.conf, I currently hard-coded the following just for scorekeeper; don't know what Jaron has planned for a more robust solution though Ellery did mention the installation script copying all statics to a central location, so settings.py might need a STATIC_ROOT set:

      Alias /static/ /opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/static/
      <Directory /opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/static>
        Require all granted
      </Directory>

```
Require all granted
```

**Note:** (JIA 1/6/2016) I had to make the following edits. FYI this was for a Debian Jessie VM running on a laptop:

   # Edit /etc/postgresql/9.4/main/pg_hba.conf to change "peer" to "md5" on the local/all/all line.

## Test

Do the following to test whether everything got set up correctly:

In a Web browser, navigate to the following URLs:

   * http://localhost/admin
   * http://localhost/dbkeeper

---
---

*[delete everything below here; keeping it around for reference for now]*

This document provides a quick description of how to build, install, and
run the application. Refer to the RaspberryPiGub page on the project wiki
for instructions on setting up hardware and a build environment prior to
proceeding with this document.

#---
# Build
#---

This is a PHP application running on a LAMP stack. There is nothing to build,
but there is a packaging script available to zip up the application to ease
deployment.

You should be able to set this up on a Raspberry Pi station by following
the steps in the Pi Setup document. To get the code from the repository
into a standard location, run the following

   $ sudo mkdir /opt/designchallenge2015
   $ sudo chown pi:pi /opt/designchallenge2015
   $ cd /opt/designchallenge2015
   $ git clone https://code.google.com/p/brata.masterserver/

<strike>
The script will begin by deleting any m.zip file that exists in the packaging
subfolder, so make sure you don't want to preserve it when running the script.

   $ cd /opt/designchallenge2015/brata.masterserver/packaging
   $ ./mkrelease.sh

This will delete and recreate a m.zip file in the current directory. The .zip
format is required for both free servers. There is also a mkrelease0.sh with a
different directory structure since the other free server needs slightly
different packaging.
</strike>


#---
# Install
#---

<strike>
Install the application into your Web server's document root:

   $ cd /var/www

Remove or move aside any exising "m" subfolder.

   $ sudo mv m{,_yyyymmdd-HHMM}

Create new folder and unzip.

   $ sudo mkdir -m 755 m
   $ cd m
   $ sudo unzip /opt/designchallenge2015/brata.masterserver/packaging/m.zip
</strike>

No installation is necessary; simply redirect the Apache configuration to
look at the workspace folder as the document root as described in the GUB,
then run the following:

   $ cd /opt/designchallenge2015/brata.masterserver/workspace/m
   $ sudo chown www-data:www-data sysconfig_data.php

Restart Apache:

   $ sudo service apache2 restart


#---
# Application setup
#---

In your Web browser, navigate to:

   http://localhost/m/setup.php

The setup page will display the following values. (TODO: There are currently
several items we don't need. I'm using code from past project and I haven't
ripped all the unused bits out.)

   Label                                      Field Value
   ------------------------------------------ -----------------------------
   Web Domain [with NO trailing slash]        http://localhost
   Web Folder[with trailing slash]            /m/
   Database Host                              localhost
   Database Name                              m
   Database User                              root
   Database Password                          $$##zxcv
   Log Level                                  5
   Send Mail (to new users)                   [checked]
   Debug Mode                                 [checked]

Set the following:

   * Uncheck Send Mail
   * Set Database Name to m
   * Set Database Password to raspberry

TODO: Create a special MySQL user account and use that username and password to
create the database, and then enter those here. If you are really building a
server farm the Database host name may be something other than localhost.

Press Submit Query. The page will transition to a Setup Complete page.

In a Web browser, navigate to:

   http://localhost/m/

On the Manage side bar along the left-hand side, click Reset Database.

The first time, leave drop-down at No Test Data and press the Reset Database
button. With this, we should be able to log-in at the main page to verify all
the database configuration and prior installation are correct.

Once everything is verified, repeat with With Test Data selected in the
drop-down and press the Reset Database button. This can take some time to build
all the test data. Once complete, a working app should be available with test
data to develop against.


#---
# Run
#---

In a Web browser, navigate to:

   http://localhost/m/

Login using the credential specified on the page.

<strike>
On the Manage side bar along the left-hand side, click Device Testing > Test
Contact.
</strike>

On the Manage side bar along the left-hand side, click Stations > CTS00 > Edit

Modify to match what's in the station config. Then submit.

Join from station.

Manage > CTS Data > Add new CTS Data
   Enter five angles for wooden prop in degrees

On the Manage side bar along the left-hand side, click rPi.

See records for all joined rPi's.

Send messages from here.

On the Manage side bar along the left-hand side, click Brata Testing.

Pick the team, pick the station.

$ tail -f /var/tmp/m.log




<strike>

To run unit tests:

   $ cd /opt/designchallenge2015/brata.station/sve/bin
   $ ./runtests

To run the SVE application for the HMB:

   $ cd /opt/designchallenge2015/brata.station/sve/bin
   $ ./sve

To monitor SVE log output in another terminal window:

   $ tail -f /var/log/syslog

To mock the MS, see the README.txt file in the wiremock subdirectory.


TODO. This document needs to be written.

Random thoughts: This started as just a single application for the
HMB Raspberry Pi unit; however, current thoughts are on combining
it with the other station(s) into a single application. Let's see
if this works.

Unless someone has a reason not to, we can run Python with the -B option so the directory doesn't get cluttered with *.pyc files.

If you run this on your Pi, you shouldn't see any output on the command line.

Open a terminal window and keep it open. In that window, type the following before running the application:

   tail -f /var/log/syslog

When you run the application, you should see something like this in the window you're running tail:

Sep 14 20:51:45 raspberrypi Constructing SVE config
Sep 14 20:51:45 raspberrypi Constructing vibration motor Huey config
Sep 14 20:51:45 raspberrypi Constructing vibration motor Dewey config
Sep 14 20:51:45 raspberrypi Constructing vibration motor Louie config
Sep 14 20:51:45 raspberrypi Constructing LED red config
Sep 14 20:51:45 raspberrypi Constructing LED yellow config
Sep 14 20:51:45 raspberrypi Constructing LED green config
Sep 14 20:51:45 raspberrypi Constructing SVE
Sep 14 20:51:45 raspberrypi Constructing vibration manager Huey
Sep 14 20:51:45 raspberrypi Constructing vibration manager Dewey
Sep 14 20:51:45 raspberrypi Constructing vibration manager Louie
Sep 14 20:51:45 raspberrypi Constructing LED red
Sep 14 20:51:45 raspberrypi Constructing LED yellow
Sep 14 20:51:45 raspberrypi Constructing LED green
Sep 14 20:51:45 raspberrypi Starting SVE.

Then, back in the window that you ran SVE, press Ctrl+C. Now in your tail window, you should see:

Sep 14 20:52:35 raspberrypi Received signal "2". Stopping SVE.
Sep 14 20:52:35 raspberrypi Stopping vibration manager Huey
Sep 14 20:52:35 raspberrypi Stopping vibration manager Dewey
Sep 14 20:52:35 raspberrypi Stopping vibration manager Louie

As you keep rerunning the application, you'll see this output in the tail window; you shouldn't see anything in the window in which you run the "sve" script.

I've disabled everything regarding the push buttons, but the code is still in there. We'll need to clean it up some time after it gets into the repository.

The Pibrella code we used the other day still needs to be put into hw.py.
</strike>
