This document provides a quick description of how to build, install, and
run the application.

#---
# Build
#---

This is a PHP application running on a LAMP stack. There is nothing to build,
but there is a packaging script available to zip up the application to ease
deployment.

#-- install the LAMP stack and dependences
apache, mod_rewrite, PHP5 PHP5-curl PHP5-mysql PHP-PDO


I recommend installing apache and making sure you can see the landing page http://localhost before adding modules.

WARNING the names of the PHP package chages by distro.  You will need the basic PHP, php curl support, php mysql support that is based on PDO.  (There are a lot of different mysql support packages you must get the PDO version).

Once you have the packages you may want to verify you can still see the landing page. http://localhost

You have to reconfigre apache to enable mod_rewrite support again this varies based on your distro

You have to edit the apache2 config files to allow overries
in /etc/apache2/apache2.conf find the lines that look like
<Directory /var/www/>
	Options Indexes FollowSymLinks
	AllowOverride None
	Require all granted
</Directory>
Chan None to all
<Directory /var/www/>
	Options Indexes FollowSymLinks
	AllowOverride All
	Require all granted
</Directory>

now restart apache. make sure you can still see the default landing page http://localhost

If all is well you can move on to installing MySql again this varies by distro.  Sometimes when you install MySql it will as you to provide a root password for the database.  MySql like most RDBMS have their own username and passwords.  Remember this password you'll need it.

Sometimes there is a seperate script you need to run to secure your install and this script will ask you to create a root DB password.

Once you have mysql installed you need to create the database.
From the command prompt try the following

mysql -u root -p
you should see recall I told you to remember your DB root password
Enter password:

If you are successful you'll see
mysql>
use the following command to create your DB
mysql> create database <a-name>

I use m for the DB name.



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

NOTE: There is also a mkrelease0.sh which makes m.zip with a different directory structure becase each free server we are using needs slightly different packaging. :(

NOTE: The .htaccess file under workspace/m was not copied. (fixed as of 10/1/10)


#---
# Install
#---

Install the application into your Web server's document root:

   $ cd /var/www
   $ sudo unzip /opt/designchallenge2015/brata.masterserver/packaging/m.zip
   $ # the following should no longer be needed
   $ sudo cp -a /opt/designchallenge2015/brata.masterserver/workspace/m/.htaccess .
   $ sudo chmod -R 755 m

To upgrade with future releases:

   $ cd /var/www
   $ sudo mv m{,_yyyymmdd-xxxx}
   $ sudo unzip /opt/designchallenge2015/brata.masterserver/packaging/m.zip
   $# should nolonger be needed
   $ sudo cp -a /opt/designchallenge2015/brata.masterserver/workspace/m/.htaccess .
   $ sudo chmod -R 755 m

#---
# Application setup
#---
open your browser and navagate to 
http://localhost/m/setup.php

You should see a form with the following labels the text in the {} indicates the form values  {checked} indicates a checked checkbox
You'll see lots of thing we aren't use -- I'm using code from past project and I have ripped all the unused bits out.

Web Folder[with trailing slash]	{/m/}
Web Domain [with NO trailing slash] {http://metsys.dlinkddns.com}	
Paypal Return URL [with NO trailing slash] {*}	
Database Host	{localhost}
Database Name	{m}
Database User	{root}
Database Password {$$##zxcv}	
Debug Mode	{checked}
Send Mail	{checked}

You'll need to change the following
uncheck Send Mail
change Database name to match the name you used in create database
change the Database Password to match your DB password.

If you are really security aware you'd create a special MySql user account and use that username and passwork to create the database and enter those here.  If you are really building a server farm the Database host name may be something other than localhost.

Once you have the form the way you want use sumbit this takes you to a
page with two links
again a.k.a back will take you back to the form 
start using application will take you to the app's landing page.

Once you are on the landing page (you should be in debug mode) you shoud set a link called reset database.

Click reset database and you'll have a form to select the test data option.  First I create the DB with no test data to verify that I have the DB name, user name, password etc correct.  If you get an error go
back to the setup.php and check your work and/or verify your install.

If all is well go back to reset database and use the test data option.
This will take a bit of time to build all thet test data if all goes well you should have a working app with test data for you to develop agains.



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
