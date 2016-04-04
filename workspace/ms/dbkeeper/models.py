from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .team_code import TeamPassCode, TeamRegCode

import json
import random

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
    registered       = models.IntegerField(default=0)

    # TODO Disabling for now; enable if needed for performance, o/w delete.    
    ## Score/time fields for the different competitions
    #rank              = models.IntegerField(default=0) # TODO Delete rank; not needed
    #launch_score      = models.IntegerField(default=0)
    #launch_duration_s = models.IntegerField(default=0)
    #dock_score        = models.IntegerField(default=0)
    #dock_duration_s   = models.IntegerField(default=0)
    #secure_score      = models.IntegerField(default=0)
    #secure_duration_s = models.IntegerField(default=0)
    #return_score      = models.IntegerField(default=0)
    #return_duration_s = models.IntegerField(default=0)

    # TODO:  Add more fields here as needed
    
    # TODO Disabling for now; enable if needed for performance, o/w delete.    
    #@property
    #def total_score(self):
    #    return self.launch_score + self.dock_score + self.secure_score + self.return_score

    #@property
    #def total_duration_s(self):
    #    # total duration of competition in seconds
    #    return self.launch_duration_s + self.dock_duration_s + self.secure_duration_s + self.return_duration_s

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
        """ Return the value of the Setting with name=name, or
            return default if Setting not found, or
            return None if no default value is specified.
        """
        try:
            return Setting.objects.get(name=name).value
        except ObjectDoesNotExist:
            return default
    
    @staticmethod
    def getLaunchParams(tri=None, vert=None):
        """ Return the whole data structure, triangle, or 1 vertex.
        
        The structure is as follows:
        [triangle0, triangle1, triangle2]
        
        where trianglen is:
        [vertex0, vertex1, vertex2, vertex3]
        
        where vertex0..2 are:
        [name, lat, lon, angle]
        
        and vertex3 (the center and triangle side length) is:
        [name, sidelength]
        
        (sidelength is really not associated with the center
        point, but is stored there for convenience.)
        
        Returns:
            the entire LAUNCH_PARAMS data structure if tri is None
            an entire triangle list if tri is not None and vert is None
            a vertex if tri and vert are not None
            None if LAUNCH_PARAMS is not in the database or cannot be parsed
        """
        try:
            launchParams = Setting.objects.get(name="LAUNCH_PARAMS").value
            launchParams = json.loads(launchParams)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return None
        
        if tri is None:
            return launchParams
        elif vert is None:
            return launchParams[tri]
        else:
            return launchParams[tri][vert]
    
    @staticmethod
    def getDockParams():
        """ Return the entire DOCK_PARAMS data structure.
        
        The structure is as follows:
        { "min_dock": <float>,
          "max_dock": <float>,
          "init_vel": <float>,
          "sim_time": int,
          "sets": [set0, set1, ..., setn-1] }
        
        where each seti is:
        { "a_aft": <float>,
          "a_fore": <float>,
          "f_rate": <float>,
          "f_qty": <float> }
        """
        try:
            dockParams = Setting.objects.get(name="DOCK_PARAMS").value
            dockParams = json.loads(dockParams)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return None
        return dockParams
    
    @staticmethod
    def getSecureParams():
        """ Generate a random problem that includes one error.
        
        Creates 4 random lock digits.  Computes the 9 tone values.
        Injects errors as specified by the Settings SECURE_NUM_INDUCED_ERRORS
        and SECURE_ERROR_DISTRIBUTION.
        
        The digits are laid out as follows (as in the Design Spec):
        
         value            index
        a  b  c          0  1  2
        d  e  f   --->   3  4  5
        g  h  i          6  7  8
        
        where [a, b, d, e] are the 4 lock digits and the other values
        are the check digits.
        
        Returns:  ([a, b, d, e], [a', b', c, d', e', f, g, h, i])
            (lockDigits, tones) - a tuple containing list of 4 integers
                                  and a list of 9 integer tone values.
                                  Some of the tone values may have been
                                  modified by an error value.
                                  All integers will be in the range 0-7.
                                  
        """
        # Choose 4 lock digits
        random.seed()  # initialize random number generator
        lockDigits = [random.randint(0,7), random.randint(0,7), random.randint(0,7), random.randint(0,7)]

        # Generate the error correcting tone sequence for the lock digits
        tones = [0]*9  # a list of 9 zeroes
        tones[0] = lockDigits[0]
        tones[1] = lockDigits[1]
        tones[2] = 7 - (tones[0] + tones[1]) % 7
        tones[3] = lockDigits[2]
        tones[4] = lockDigits[3]
        tones[5] = 7 - (tones[3] + tones[4]) % 7
        tones[6] = 7 - (tones[0] + tones[3]) % 7
        tones[7] = 7 - (tones[1] + tones[4]) % 7
        tones[8] = 7 - (tones[2] + tones[5]) % 7
        
        # Try to retrieve error injection values from the Setting table
        try:
            errorValues = json.loads(Setting.objects.get(name="SECURE_ERROR_DISTRIBUTION").value)
            numErrors   = int(Setting.objects.get(name="SECURE_NUM_INDUCED_ERRORS").value)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return None
        
        # Throw in numErrors random errors
        unused = range(0,9)  # create a list of indices that could be zapped
        while numErrors:
            errorDigit = random.choice(unused)  # choose one of the intact tone values to mess up
            change = random.choice(errorValues)  # choose an amount to perturb it by
            tones[errorDigit] = (tones[errorDigit] + change) % 7  # add the corruption
            unused.remove(errorDigit)  # don't choose the same one twice
            numErrors -= 1
        
        return (lockDigits, tones)

    @staticmethod
    def getReturnParams(station_id=None, value=None):
        """ Return the whole data structure, a station, or a value.
        
        Stations are indexed by the station_id (case-sensitive).
        Values are indexed 0-5.
        
        The structure is as follows:
            {
              "return01": station1,
              "return02": station2,
               ...,
              "return06": station6
            }
        
        where stationn is:
            [value1, value2, ..., value6]
        
        Returns:
            the entire RETURN_PARAMS data structure if station_id is None
            the data for a station if station_id is not None and value is None
            an individual data value if station_id and value are not None
        """
        try:
            returnParams = Setting.objects.get(name="RETURN_PARAMS").value
            returnParams = json.loads(returnParams)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return None
        try:
          if station_id is None:
            return returnParams
          elif value is None:
            return returnParams[station_id]
          else:
            return returnParams[station][value]
        except (ObjectDoesNotExist, ValueError, TypeError):
            return None
        
    
    def __unicode__(self):
        return self.name
    
