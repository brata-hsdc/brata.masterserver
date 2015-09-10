from django.db import models
from django.utils import timezone

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
    class Meta:
        managed = True  # We want manage.py to migrate database changes for us
    
    # Constants
    DATA_FIELD_LENGTH = 2000
    MESSAGE_FIELD_LENGTH = 100

    # Values for type
    UNKNOWN_TYPE      = -1
    REGISTER_MSG_TYPE = 1
    CHECKIN_TYPE      = 2
    ADDORG_TYPE       = 3
    ADDUSER_TYPE      = 4
    ADDTEAM_TYPE      = 5

    TYPE_CHOICES = (
                    (UNKNOWN_TYPE,      "Unknown"),
                    (REGISTER_MSG_TYPE, "Register"),
                    (CHECKIN_TYPE,      "Check In"),
                    (ADDORG_TYPE,       "Add Organization"),
                    (ADDUSER_TYPE,      "Add User"),
                    (ADDTEAM_TYPE,      "Add Team"),
                   )
    
    # Values for status
    FATAL_STATUS    = -10  # a message indicating a serious or fatal problem
    WARNING_STATUS  = -5   # a message indicating a non-fatal problem
    FAIL_STATUS     = -1   # an event that resulted in an error
    UNKNOWN_STATUS  = 0
    SUCCESS_STATUS  = 1    # an event that was completed without error
    DETAIL_STATUS   = 3    # less significant information messages
    INFO_STATUS     = 5    # significant information messages
    
    STATUS_CHOICES = (
                      (FATAL_STATUS,   "Fatal"),
                      (WARNING_STATUS, "Warning"),
                      (FAIL_STATUS,    "Fail"),
                      (UNKNOWN_STATUS, "Unknown"),
                      (SUCCESS_STATUS, "Success"),
                      (INFO_STATUS,    "Info"),
                      (DETAIL_STATUS,  "Detail"),
                     )
    
    # Schema definition
    time    = models.DateTimeField(auto_now_add=True) # automatically set the current datetime on creation
    type    = models.SmallIntegerField(choices=TYPE_CHOICES, default=UNKNOWN_TYPE)
    team    = models.ForeignKey("dbkeeper.Team", null=True)  # give name as string to avoid cyclic import dependency
    pi      = models.ForeignKey(PiStation, null=True)
    status  = models.SmallIntegerField(choices=STATUS_CHOICES, default=UNKNOWN_STATUS)
    data    = models.TextField(blank=True, null=True)
    message = models.CharField(max_length=MESSAGE_FIELD_LENGTH, blank=True)
    
    @staticmethod
    def createEvent(type=None, team=None, pi=None, status=None, data=None, message=None):
        """ Convenience function that makes and returns a new PiEvent, but caller must call ev.save() """
        ev = PiEvent(type=type, team=team, pi=pi, status=status, data=data, message=message)
        if type is None:
            type = PiEvent.UNKNOWN_TYPE
        if status is None:
            status = PiEvent.UNKNOWN_STATUS
        if message is None:
            message = ""
        return ev
    
    @staticmethod
    def addEvent(type=None, team=None, pi=None, status=None, data=None, message=None):
        """ Convenience function that makes, saves, and returns a new PiEvent """
        ev = PiEvent.createEvent(type=type, team=team, pi=pi, status=status, data=data, message=message)
        ev.save()
        return ev

    def __unicode__(self):
        return "{}: {}".format(self.time, self.message)

        