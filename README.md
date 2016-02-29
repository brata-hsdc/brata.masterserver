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

Download Raspbian Jessie Lite released 2016-02-09 from https://www.raspberrypi.org/downloads/raspbian/.
Note that for this next step the memory you use will make a big difference on the performance of your server.  After research and testing for 2016 the following card was selected as the best balance of write speed, read speed and cost: SanDisk Extreme 16GB microSDHC UHS-1 Card with Adapter (SDSQXNE-016G-GN6MA).
It is also suggested to run the server on a Pi 2 as the extra CPU power will definitely help.
Unzip the zip file to get the raw SD card image. Write the raw image file to the SD card:

```sh
$ sudo dd if=2016-02-09-raspbian-jessie-lite.img of=/dev/sdX bs=4M
$ sudo sync
```

Eject SD card, insert into device, and power up.

Log-in when prompted.
type the following to change the password from the default of raspberry
THIS IS VERY IMPORTANT or your Pi will likely be hacked in less than 24 hrs if on a public network
```sh
$ passwd
```

### If using wired skip this, otherwise if using a wifi dongle you will need to join your network first
```sh
$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
Add to the bottom of the file
```sh
network={
  ssid="YOUR_SSID"
  psk="YOUR_NETWORK_PASSWORD"
}
```
Save the file Ctrl-x and yes. Then reboot.
```sh
$ sudo reboot
```

Next fix some of the basic settings
```sh
$ sudo raspi-config
```
Here you need to select to:
1) Expand the file system
2) Use option 5 and then option I1 to change the local to en_US.UTF-8 and change it to the default
3) Use option 5 again and then I2 to select your time zone
4) Use option 5 again and then I3 here:
   Leave it at the default keyboard it came up with but on the nex page after selecting it go to other instead of the UK options.  This way you can then select English (US) and then select all the defaults afte that.
5) Select option 9 for advanced options and change your host name to something standardized by yoru group which includes the station type and number, such as ms01, return01, dock01, secure01, then increase for each duplicated station type.
6) If/When the team decides it is needed use option 4 to enable wait for network at boot.
Upon exit the pi will restart and enable the selected changes.

### Update Repositories and in case remote QRCode generation goes down add QRCode generation support
### NOTE The first install line goes all the way out and ends with python-tk so when you copy keep scrolling over
```sh
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
$ sudo apt-get install git
$ sudo apt-get install python-imaging
$ sudo apt-get install python-pip
$ sudo pip install pillow
$ sudo pip install qrcode
```

### Install Python dev to enable mod_wsgi install
```sh
$ sudo apt-get install python-dev
```

Ah crud need to reinstall python from source with --enabled-shared? This error came from mod_wsgi install.  Suggests there will be major performance and memory hit if not done. NOTE I could not find the details of this, whomever put it in if it could please be clarified?

### Install the Apache Web Server
```sh
$ sudo apt-get install apache2
```

### Install mod_wsgi
```sh
$ sudo apt-get install apache2-threaded-dev
$ sudo pip install mod_wsgi
$ sudo apt-get install libapache2-mod-wsgi
$ sudo a2enmod wsgi <TBD is this really needed?>
```

### Install Gunicorn

[*Gunicorn*](http://gunicorn.org/) is a lightweight Python-based web server that can be used in place of the Apache server.
It should perform better than Apache.  We have observed several-second delays with Apache when handling requests.

```sh
$ sudo pip install gunicorn
```

#### Make Gunicorn run at boot
TO DO:  add instructions

#### Serving static files with Gunicorn
Gunicorn can't serve the static files for our Django apps.
Django can be configured to serve them up, or we can set up [*Nginx*](http://nginx.org/).
```sh
$ sudo apt-get install nginx
```
TODO giving up here says installed nginx but can't start because is not configured

### Install PostgreSQL
```sh
$ sudo apt-get install postgresql-9.4
```

### Install psycopg2
```sh
$ sudo apt-get install python-psycopg2
```

TODO do we need to create a virtual environment first?

### Install Django
```sh
$ sudo pip install Django
```

### Install pytz
`pytz` makes it easy to construct a proper *tzinfo* to set the timezone in Django.  This
allows UTC datetimes to be stored in the database, but displayed in the local timezone.
The local timezone is set in the Django **settings.py** file.

```sh
$ sudo pip install pytz
```

### Install httpie

`httpie` is a command line tool that has a lot of the same functionality as `curl` and `wget`, but with
a more user-friendly command line structure, and colorful syntax highlighting.  See the
[httpie website](http://httpie.org) for more info.

`httpie` is written in Python, so it can be installed with `pip`, like this:

```sh
$ sudo pip install httpie
```

## Setup

### Create the database
Create a new PostgreSQL database called `msdb`.
```sh
$ cd /usr/lib/postgresql/9.4/bin
$ sudo -u postgres psql
# create database msdb;
# create user pi password '<get from team>';
# grant all privileges on database msdb to pi;
# \q
```

### Clone this repository
```sh
$ sudo mkdir /opt/designchallenge2016
$ sudo chown pi:pi /opt/designchallenge2016
$ cd /opt/designchallenge2016
$ git clone https://github.com/brata-hsdc/brata.masterserver.git
```

### Modify the Apache configuration
```sh
$ sudo nano /etc/apache2/sites-enabled/000-default.conf
```
replace
DocumentRoot /var/www/html
with
```sh
Alias /static/ /opt/designchallenge2016/brata.masterserver/workspace/ms/static/

<Directory /opt/designchallenge2016/brata.masterserver/workspace/ms/static>
<Files wsgi.py>
Order deny,allow
Allow from all
</Files>
</Directory>

WSGIScriptAlias / /opt/designchallenge2016/brata.masterserver/workspace/ms/ms/wsgi.py
<Directory /opt/designchallenge2016/brata.masterserver/workspace/ms/ms>
<Files wsgi.py>
Order deny,allow
Allow from all
</Files>
</Directory>
```

### Install the hidden configuration files

### Install the ms Django project and initialize the DB
### TODO Note this backup file currently throws errors because it is the only way to create a full backup with the current circular dependency. After the dependency issue is fixed this should be resnapshotted with data only and no longer throw errors.  At that time we will also need to add the user creation here.
```sh
$ cd /opt/designchallenge2016/brata.masterserver/workspace/ms/ms
$ python manage.py migrate
$ sudo -u postgres psql -d msdb < db_backup.sql
```

**Note:** (JIA 12/17/2015) I had to make the following edits. FYI this was for a Debian Jessie VM running on a laptop:

   # Edit /opt/.../workspace/ms/ms/settings.py and set HOST to localhost in order to get migrate to run successfully. 
   # Edit /etc/apache2/envvars to change APACHE_RUN_USER and APACHE_RUN_GROUP from www-data to the development user; restart apache2.
   # In the /etc/apache2/sites-enabled/000-default.conf, added after "Allow from all", then restarted Apache:
   # In the /etc/apache2/sites-enabled/000-default.conf, I currently hard-coded the following just for scorekeeper; don't know what Jaron has planned for a more robust solution though Ellery did mention the installation script copying all statics to a central location, so settings.py might need a STATIC_ROOT set  TODO Houston we have a problem as there is already a static alias which was missing and has been added in, but it was different then the one here, so now we have two static sitest to server one will need to be changed.  Although with the improvement from gunicorn they both should be migrated to however we chose to do it the new way:

      Alias /static/ /opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/static/
      <Directory /opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/static>
        Require all granted
      </Directory>

```
Require all granted
```

**Note:** (JIA 1/6/2016) I had to make the following edits. FYI this was for a Debian Jessie VM running on a laptop:

   # Edit /etc/postgresql/9.4/main/pg_hba.conf to change "peer" to "md5" on the local/all/all line.

#### Stop Apache and start Gunicorn

First stop the Apache service if it is running, then
start Gunicorn and have it listen on the interface specified by <ip addr> (the server's IP address) port 80.
NOTE TODO we need to get rid of this once we figure out starting it as a service. 

```sh
$ sudo service apache2 stop
$ cd /opt/designchallenge2016/brata.masterserver/workspace/ms
$ sudo gunicorn -b <ip addr>:80 --workers=3 ms.wsgi
```

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
