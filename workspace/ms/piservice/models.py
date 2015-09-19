from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import random

from dbkeeper.models import Setting

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
    HOST_FIELD_LENGTH       = 60  # might need to hold FQDN
    STATION_ID_FIELD_LENGTH = 20
    
    # Values for type
    UNKNOWN_STATION_TYPE = 0
    RTE_STATION_TYPE     = 1
    # TODO: add other types as appropriate
    STATION_TYPE_CHOICES = (
                             (UNKNOWN_STATION_TYPE, "Unknown"),
                             (RTE_STATION_TYPE,     "Return to Earth (RTE)"),
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
    
    PI_TYPE_STRINGS = (
                         ("A+", A1PLUS_PI_TYPE),
                         ("B+", B1PLUS_PI_TYPE),
                         ("B2", B2_PI_TYPE),
                         ("B",  B1_PI_TYPE),
                         ("A",  A1_PI_TYPE),
                      )
    
    # Schema definition
    host            = models.CharField(max_length=HOST_FIELD_LENGTH, blank=True)
    pi_type         = models.PositiveSmallIntegerField(choices=PI_TYPE_CHOICES, default=UNKNOWN_PI_TYPE)
    station_type    = models.PositiveSmallIntegerField(choices=STATION_TYPE_CHOICES, default=UNKNOWN_STATION_TYPE)
    station_id      = models.CharField(max_length=STATION_ID_FIELD_LENGTH, blank=True)
    joined          = models.ForeignKey("PiEvent", null=True, on_delete=models.SET_NULL)
    
    @staticmethod
    def piType(typeStr):
        """ Try to convert a string into one of the known Pi Type choices """
        for s,t in PiStation.PI_TYPE_STRINGS:
            if s in typeStr:
                return t
        return PiStation.UNKNOWN_PI_TYPE
    
    @staticmethod
    def allowedHost(host):
        """ Verify that the host is in STATION_IPS """
        try:
            return host in Setting.get("STATION_IPS").strip().split()
        except ObjectDoesNotExist:
            return False
        
    @staticmethod
    def validateStation(host, station_id):
        """ Return a PiStation object that matches host and station_id, or return None """
        try:
            station = PiStation.objects.get(host=host, station_id=station_id)
        except ObjectDoesNotExist:
            station = None
        return station
    
    def setStationId(self):
        """ Create a unique station_id value.
        
            The station_id is guaranteed to be unique because it contains
            the record id, which is unique.  However, the station_id cannot
            be constructed until the record has been saved, because that is
            when the record id is created.
        """
        # The station_id is guaranteed to be unique because it contains
        # the record id, which is unique.
        st_id = "{}:{:04x}".format(self.id, random.getrandbits(4*4))
        self.station_id = st_id
        return st_id
    
    def __unicode__(self):
        return "{} ({} | {})".format(self.host, self.station_id, self.station_type)
        
    
#----------------------------------------------------------------------------
class PiEvent(models.Model):
    """ A time-stamped instance of a specific occurrence, what kind of
        occurrence it was, who did it, and possibly a reference to some
        other data.
    """
    class Meta:
        managed = True  # We want manage.py to migrate database changes for us
        ordering = ['time']
    
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
    JOIN_MSG_TYPE     = 6
    LEAVE_MSG_TYPE    = 7
    STATION_STATUS_MSG_TYPE = 8

    TYPE_CHOICES = (
                    (UNKNOWN_TYPE,      "Unknown"),
                    (REGISTER_MSG_TYPE, "Register"),
                    (CHECKIN_TYPE,      "Check In"),
                    (ADDORG_TYPE,       "Add Organization"),
                    (ADDUSER_TYPE,      "Add User"),
                    (ADDTEAM_TYPE,      "Add Team"),
                    (JOIN_MSG_TYPE,     "Join"),
                    (LEAVE_MSG_TYPE,    "Leave"),
                    (STATION_STATUS_MSG_TYPE, "Station Status"),
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
    team    = models.ForeignKey("dbkeeper.Team", null=True, on_delete=models.SET_NULL)  # give name as string to avoid cyclic import dependency
    pi      = models.ForeignKey(PiStation, null=True, on_delete=models.SET_NULL)
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

        