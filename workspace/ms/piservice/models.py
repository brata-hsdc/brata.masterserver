from django.db import models
from dbkeeper.models import Team

# See the schema diagram and other documentation in the
# brata.workstation/transitions folder.

#----------------------------------------------------------------------------
class PiStation(models.Model):
    """ Holds information about the Raspberry Pi stations being used in the
        competition.
    """
    class Meta:
        managed = True  # We want manage.py to migrate database changes for us
    
    # Constants
    HOST_FIELD_LENGTH  = 60  # might need to hold FQDN
    
    # Values for type
    UNKNOWN_STATION_TYPE = 0
    # TODO: add other types as appropriate
    STATION_TYPE_CHOICES = (
                             (UNKNOWN_STATION_TYPE, "Unknown"),
                           )
    
    UNKNOWN_PI_TYPE = 0
    A1_PI_TYPE      = 1
    A1PLUS_PI_TYPE  = 2
    B1_PI_TYPE      = 3
    B1PLUS_PI_TYPE  = 4
    B2_PI_TYPE      = 5
    # TODO: add other types as appropriate
    PI_TYPE_CHOICES = (
                        (UNKNOWN_PI_TYPE, "Unknown"),
                        (A1_PI_TYPE,      "Gen 1 Model A"),
                        (A1PLUS_PI_TYPE,  "Gen 1 Model A+"),
                        (B1_PI_TYPE,      "Gen 1 Model B"),
                        (B1PLUS_PI_TYPE,  "Gen 1 Model B+"),
                        (B2_PI_TYPE,      "Gen 2 Model B"),
                      )
    
    # Schema definition
    host            = models.CharField(max_length=HOST_FIELD_LENGTH, blank=True)
    station_type    = models.PositiveSmallIntegerField(choices=STATION_TYPE_CHOICES, default=UNKNOWN_STATION_TYPE)
    pi_type         = models.PositiveSmallIntegerField(choices=PI_TYPE_CHOICES, default=UNKNOWN_PI_TYPE)
    stationInstance = models.PositiveSmallIntegerField(default=0)
    
#----------------------------------------------------------------------------
class PiEvent(models.Model):
    """ A time-stamped instance of a specific occurrence, what kind of
        occurrence it was, who did it, and possibly a reference to some
        other data.
    """
    # Constants
    DATA_FIELD_LENGTH = 2000
    MESSAGE_FIELD_LENGTH = 100

    # Values for type
    UNKNOWN_TYPE = -1
    REGISTER_MSG_TYPE = 1

    TYPE_CHOICES = (
                    (UNKNOWN_TYPE, "Unknown"),
                    (REGISTER_MSG_TYPE, "Register"),
                   )
    
    # Values for status
    UNKNOWN_STATUS = -1
    FAIL_STATUS    = 0
    SUCCESS_STATUS = 1
    
    STATUS_CHOICES = (
                      (UNKNOWN_STATUS, "Unknown"),
                      (FAIL_STATUS, "Fail"),
                      (SUCCESS_STATUS, "Success"),
                     )
    
    # Schema definition
    time    = models.TimeField()
    type    = models.SmallIntegerField(choices=TYPE_CHOICES, default=UNKNOWN_TYPE)
    team_id = models.ForeignKey(Team)
    pi_id   = models.ForeignKey(PiStation)
    status  = models.SmallIntegerField(choices=STATUS_CHOICES, default=UNKNOWN_STATUS)
    data    = models.TextField(blank=True)
    message = models.CharField(max_length=MESSAGE_FIELD_LENGTH, blank=True)
    