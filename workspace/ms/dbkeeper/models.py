from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .team_code import TeamPassCode, TeamRegCode

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
# class UserMSUser(models.Model):
#     user = models.OneToOneField(User)


#----------------------------------------------------------------------------
class Organization(models.Model):
    class Meta:
        managed = True  # We want manage.py to migrate database changes for us

    # Constants
    NAME_FIELD_LENGTH = 100
    
    # Values for type
    UNKNOWN_TYPE = 0
    SCHOOL_TYPE  = 1
    HSDC_TYPE    = 2
    TYPE_CHOICES = ((UNKNOWN_TYPE, "Unknown"),
                    (SCHOOL_TYPE,  "School"),
                    (HSDC_TYPE,    "HSDC"),
                   )
    
    # Schema definition
    name = models.CharField(max_length=NAME_FIELD_LENGTH, unique=True)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=UNKNOWN_TYPE)
    
    def __unicode__(self):
        return self.name
    
#----------------------------------------------------------------------------
class Team(models.Model):
    class Meta:
        managed = True  # We want manage.py to migrate database changes for us
    
    # Constants
    NAME_FIELD_LENGTH      = 100  # Make it long because some team will have a "creative" name
    PASS_CODE_FIELD_LENGTH = 50
    REG_CODE_FIELD_LENGTH  = 32
    
    # Schema definition
    name             = models.CharField(max_length=NAME_FIELD_LENGTH, unique=True)
    organization     = models.ForeignKey(Organization)
    pass_code        = models.CharField(max_length=PASS_CODE_FIELD_LENGTH, blank=True)
    reg_code         = models.CharField(max_length=REG_CODE_FIELD_LENGTH, blank=True)
    registered       = models.ForeignKey("piservice.PiEvent", null=True, related_name="teams")  # give name as string to avoid cyclic import dependency
    
    #    Score fields for the different competitions
    total_score      = models.IntegerField(default=0)
    total_duration_s = models.IntegerField(default=0)  # total duration of competition in seconds
    # TODO:  Add more fields here as needed
    
    @staticmethod
    def makeTeamCode(existingCodes=None):
        """ Create a unique pass_code for the team """
        return TeamPassCode.newPassCode(list(Team.objects.values_list("pass_code")))
    
    @staticmethod
    def generateRegCode():
        """ Create a unique reg_code for the team """
        return TeamRegCode.newRegCode(list(Team.objects.values_list("reg_code")))
    
    def checkRegCode(self, code):
        """ Return True if code == this team's reg_code field.
            This method ignores case and leading or trailing whitespace.
        """
        return code.strip().lower() == self.reg_code
    
    def __unicode__(self):
        return self.name
    
#----------------------------------------------------------------------------
class MSUser(models.Model):
    """ Represents information about a team mentor, teacher, chaperone, student,
        MS administrator, etc.
        There will be one of these for anyone who will log in to the MS system
        and needs some level of permission above what is open to all users.
    """
    class Meta:
        managed = True  # We want manage.py to migrate database changes for us

    # Constants
    NAME_FIELD_LENGTH  = 100
    PHONE_FIELD_LENGTH = 20
    
    # Schema definition
#     name         = models.CharField(max_length=NAME_FIELD_LENGTH, unique=True)
    organization = models.ForeignKey(Organization)
    work_phone   = models.CharField(max_length=PHONE_FIELD_LENGTH, blank=True)
    mobile_phone = models.CharField(max_length=PHONE_FIELD_LENGTH, blank=True)
    other_phone  = models.CharField(max_length=PHONE_FIELD_LENGTH, blank=True)
    note         = models.TextField(blank=True)
    teams        = models.ManyToManyField(Team)
    user         = models.OneToOneField(User)
    
    def __unicode__(self):
        return "{} {} ({}) - {}".format(self.user.first_name,
                                        self.user.last_name,
                                        self.user.username,
                                        self.organization.name)

#----------------------------------------------------------------------------
class Setting(models.Model):
    """ Simple table to hold application settings.
    
        Each row in the table has setting name and value.  The value will be
        stored as a string.  It is up to the application to parse the string.
        
        Other code in the app can easily access Setting values using the get()
        static method.
        
        Examples:
        
           timeout = Setting.get("REFRESH_INTERVAL_MS", default=2000)  # returns 2000 if name not found
           timeout = Setting.get("REFRESH_INTERVAL_MS")                # returns None if name not found
    """
    class Meta:
        managed = True  # We want manage.py to migrate database changes for us
        
    # Constants
    NAME_FIELD_LENGTH  = 50

    # Schema definition
    name        = models.SlugField(max_length=NAME_FIELD_LENGTH, unique=True)
    value       = models.TextField(blank=True)
    description = models.TextField(blank=True)
    
    @staticmethod
    def get(name, default=None):
        """ Return the value of the Setting with name=name.
            Return default if Setting not found.  Return
            None if no default value is specified.
        """
        try:
            return Setting.objects.get(name=name).value
        except ObjectDoesNotExist:
            return default
        
    def __unicode(self):
        return self.name
    