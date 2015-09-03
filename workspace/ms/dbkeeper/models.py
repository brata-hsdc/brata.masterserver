from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# See the schema diagram and other documentation in the
# brata.workstation/transitions folder.

# TODO:  Questions for Jaron about the 2015 design:
#        1. Do we need the competitors and mentors to register with real
#           user accounts?  (I plan to use Django's built-in authentication.)
#        2. What is the emailAddress ("email" in the old db) field used for?
#        3. Do we need the fine-grained permissions that last year's db has?
#           It looks like there were just 2 roles defined:  ADMIN (all perms)
#           and NONE (no perms).

#----------------------------------------------------------------------------
# Adding profile information to the Django User class using what they call
# a "profile model" that is linked to the User model with a one-to-one
# relationship.  (See the explanation here:
# https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model)
#
# The default User class already contains username, password, email, first_name,
# last_name.  If that's all we need, we don't have to do this at all.
class Admin(models.Model):
    user = models.OneToOneField(User)

#----------------------------------------------------------------------------
class School(models.Model):
    class Meta:
        managed = True  # We want manage.py to migrate database changes for us

    # Constants
    NAME_FIELD_LENGTH = 100
    
    # Schema definition
    name = models.CharField(max_length=NAME_FIELD_LENGTH, unique=True)
    
#----------------------------------------------------------------------------
class Team(models.Model):
    class Meta:
        managed = True  # We want manage.py to migrate database changes for us
    
    # Constants
    NAME_FIELD_LENGTH = 100  # Make it long because some team will have a "creative" name
    PIN_FIELD_LENGTH  = 20
    
    # Schema definition
    name            = models.CharField(max_length=NAME_FIELD_LENGTH, unique=True)
    school          = models.ForeignKey(School)
    pin             = models.CharField(max_length=PIN_FIELD_LENGTH, default="generated")  # TODO: what's this for? Do we need it or will the password be sufficient?
    
    #    Score fields for the different competitions
    totalScore      = models.IntegerField(default=0)
    totalDuration_s = models.IntegerField(default=0)  # total duration of competition in seconds
    # TODO:  Add more fields here as needed
    
#----------------------------------------------------------------------------
class Mentor(models.Model):
    """ Represents information about a team mentor, teacher, chaperone:  a
        person of authority who represents the team and/or is a POC.
    """
    class Meta:
        managed = True  # We want manage.py to migrate database changes for us

    # Constants
    NAME_FIELD_LENGTH  = 100
    PHONE_FIELD_LENGTH = 20
    
    # Schema definition
    name        = models.CharField(max_length=NAME_FIELD_LENGTH, unique=True)
    school      = models.ForeignKey(School)
    workPhone   = models.CharField(max_length=PHONE_FIELD_LENGTH, blank=True)
    mobilePhone = models.CharField(max_length=PHONE_FIELD_LENGTH, blank=True)
    otherPhone  = models.CharField(max_length=PHONE_FIELD_LENGTH, blank=True)
    note        = models.TextField(blank=True)
    teams       = models.ManyToManyField(Team)
    