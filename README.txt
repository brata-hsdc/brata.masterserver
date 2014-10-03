This document provides a quick description of how to build, install, and
run the application.

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

The script will begin by deleting any m.zip file that exists in the packaging
subfolder, so make sure you don't want to preserve it when running the script.

   $ cd /opt/designchallenge2015/brata.masterserver/packaging
   $ ./mkrelease.sh

This will delete and recreate a m.zip file in the current directory. The .zip
format is required for both free servers. There is also a mkrelease0.sh with a
different directory structure since the other free server needs slightly
different packaging.


#---
# Install
#---

Install the application into your Web server's document root:

   $ cd /var/www

Remove or move aside any exising "m" subfolder.

   $ mv m{,_yyyymmdd-HHMM}

Create new folder and unzip.

   $ sudo mkdir -m 755 m
   $ cd m
   $ sudo unzip /opt/designchallenge2015/brata.masterserver/packaging/m.zip
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
   Web Folder[with trailing slash]            /m/
   Web Domain [with NO trailing slash]        http://metsys.dlinkddns.com
   Paypal Return URL [with NO trailing slash] *
   Database Host                              localhost
   Database Name                              m
   Database User                              root
   Database Password                          $$##zxcv
   Debug Mode                                 [checked]
   Send Mail                                  [checked]

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

On the Manage side bar along the left-hand side, click Device Testing > Test
Contact.




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
