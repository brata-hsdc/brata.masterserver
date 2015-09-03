# Master Server Deployment

## Install Python, Django, ...

## Install the Django project

## Configure the Apache config

(Apache needs a WSGI extension I think.  See the Django deployment docs.)

## Configure the `ms/settings.py`

### Set the database parameters to access the PostgreSQL server

### Change the SECRET_KEY

### Turn off DEBUG

## See the Django deployment checklist

Take a look at the []Django Deployment Checklist]()https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/).

## Database Maintenance

### Backup the database contents (pg_dump)

```sh
# pg_dump -U pi msdb | bzip2 >  msdb_dump_`date +yyyymmdd-HHMMSS`.bz2
```
*[TODO:  double-check this command syntax]*

### Restore the database contents

```sh
# bzcat <msdb_dump_file>.bz2 | psql -U pi -d msdb 
```
*[TODO:  double-check this command syntax]*
