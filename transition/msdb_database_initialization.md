# MSDB Database Initialization

Django can do most of the database setup work.  However, you need a few
prerequisites, and then you need to perform the following bootstrap process.

## Prerequisites

1. **Python 2.7** installed
2. **PostgreSQL** installed
3. `brata.masterserver/ms project` installed (copied to *`[put folder here]`*)
4. Your computer has a user account with username "pi"

## Names you can configure

This document uses the following identifiers and values in its examples.
You may want to substitute different values for your configuration.

Identifier | Meaning
-----------|--------
pi         | system account user name and database user name
raspberry  | system password for user "pi" and database password for user "pi"
msdb       | Master Server database name

## Procedure

## 1. Create a database user named "pi" and a database named "msdb"

Use the `psql` command line utility that comes with PostgreSQL.  You can
also accomplish the same thing through the `pgadmin` GUI, but it is harder
to explain here.

```
# psql -U postgres
psql (9.4.4)
WARNING: Console code page (437) differs from Windows code page (1252)
         8-bit characters might not work correctly. See psql reference
         page "Notes for Windows users" for details.
Type "help" for help.

postgres=# CREATE USER pi WITH PASSWORD 'raspberry';
CREATE ROLE
postgres=# CREATE DATABASE msdb;
CREATE DATABASE
postgres=# GRANT ALL PRIVILEGES ON DATABASE msdb TO pi;
GRANT
postgres=# \q
```

Now you should have an empty database.

## 2. Initialize the database structure

This is done by Django's `manage.py` utility.  It will create tables based
on the Django models in our code.

If you were starting from scratch, you would do `makemigrations` to scan the
models and generate the operations needed to modify the database to reflect
those models.  However, if you cloned the `ms` code repository, those migrations
have already been generated.  You just need to apply them.

So you **do not need** to do this:

```
# python manage.py makemigrations
Migrations for 'piservice':
  0001_initial.py:
    - Create model PiEvent
    - Create model PiStation
    - Add field piID to pievent
    - Add field teamID to pievent
Migrations for 'dbkeeper':
  0001_initial.py:
    - Create model Admin
    - Create model Mentor
    - Create model School
    - Create model Team
    - Add field school to mentor
    - Add field teams to mentor
```

You can apply the migrations that already exist in the Django project to the
database using the `migrate` command to `manage.py`, like this:

```
# python manage.py migrate
Operations to perform:
  Synchronize unmigrated apps: staticfiles, messages
  Apply all migrations: sessions, admin, auth, contenttypes, piservice, dbkeeper
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
  Installing custom SQL...
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying dbkeeper.0001_initial... OK
  Applying piservice.0001_initial... OK
  Applying sessions.0001_initial... OK
```

Now you should have a database with tables named School, Mentor, Team,
PiStation, PiEvent, and a few other Django administrative tables.

## 3. Load content into the database

We can pre-populate the database with some initial content for testing
during development.  We could also use the same technique to load up any
real-content on game day that we were able to prepare in advance.  This
example uses a file called `initial_content.sql`, but there will probably
be multiple of these files:  some for testing, and some for actual deployment.

```
# psql -U pi msdb < initial_content.sql
```

`initial_content.sql` would be a file created using the `pg_dump` command
to dump the contents of a previous version of the `msdb` database.

## 4. Create a Django *superuser*

You will need this to log into the Django *admin* interface.

```
# python manage.py createsuperuser
Username (leave blank to use 'ellery'): pi
Email address:
Password: raspberry
Password (again): raspberry
Superuser created successfully.
```

## 5. See if it worked

To see if it worked, connect to the Django app's *admin* interface using your
web browser.  If you already have the Django app deployed in Apache, just
visit http://localhost/admin/.

If you don't have Apache running, run the Django development server, like this:

```
# python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
August 30, 2015 - 19:34:36
Django version 1.8.3, using settings 'ms.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Then connect to it with this URL:  http://localhost:8000/admin

You should see the Django login screen.

After logging in successfully, you should see the top level of the
*Django administration* panel.  From there you can add other
administrative and non-adminstrative users and assign them to groups with
specific permissions.
