# MSDB Database Initialization

Django can do most of the database setup work.  However, you need a few
prerequisites, and then you need to perform the following bootstrap process.

## Prerequisites

1. **Python 2.7** installed
2. **PostgreSQL** installed
3. `brata.masterserver/ms project` installed (copied to *`[put folder here]`*)
4. Your computer has a user account with username "pi"

## Procedure

## 1. Create a database user named "pi" and a database named "msdb"

Use the `psql` command line utility that comes with PostgreSQL.  You can
also accomplish the same thing through the `pgadmin` GUI, but it is harder
to explain here.

```
> psql -U postgres
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

```
> python manage.py makemigrations
> python manage.py migrate
```

Now you should have a database with tables named School, Mentor, Team,
PiStation, PiEvent, and a few other Django administrative tables.

## 3. Load content into the database

We can pre-populate the database with some initial content for testing
during development.  We could also use the same technique to load up any
real-content on game day that we were able to prepare in advance.

```
> psql -U pi msdb < initial_content.sql
```

The `initial_content.sql` file is created using the `pg_dump` command.
