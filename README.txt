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

This will create a m.zip file in the current directory.

NOTE: The .htaccess file under workspace/m was not copied. (TODO)


#---
# Install
#---

Install the application into your Web server's document root:

   $ cd /var/www
   $ sudo mkdir -m 755 m
   $ cd m
   $ sudo unzip /opt/designchallenge2015/brata.masterserver/packaging/m.zip
   $ sudo cp -a /opt/designchallenge2015/brata.masterserver/workspace/m/.htaccess .

To upgrade with future releases:

   $ cd /var/www
   $ sudo mv m{,_yyyymmdd-xxxx}
   $ sudo mkdir -m 755 m
   $ cd m
   $ sudo unzip /opt/designchallenge2015/brata.masterserver/packaging/m.zip
   $ sudo cp -a /opt/designchallenge2015/brata.masterserver/workspace/m/.htaccess .


#---
# Run
#---

Restart Apache if desired, but not required:

   $ sudo /etc/init.d/apache2 restart

In a Web browser, navigate to:

   http://localhost/m/

TODO: 404 Not Found.


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
