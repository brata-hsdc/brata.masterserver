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
    HOST_FIELD_LENGTH         = 60  # might need to hold FQDN
    STATION_ID_FIELD_LENGTH   = 20
    STATION_TYPE_FIELD_LENGTH = 20
    SERIAL_NUM_FIELD_LENGTH   = 50
    URL_FIELD_LENGTH          = 200
    
    # Values for type
    UNKNOWN_STATION_TYPE = "Unknown"
    LAUNCH_STATION_TYPE  = "Launch"
    DOCK_STATION_TYPE    = "Dock"
    SECURE_STATION_TYPE  = "Secure"
    RETURN_STATION_TYPE  = "Return"
    
    # TODO: add other types as appropriate
    STATION_TYPE_CHOICES = (
                             (UNKNOWN_STATION_TYPE, "Unknown"),
                             (LAUNCH_STATION_TYPE,  "Launch"),
                             (DOCK_STATION_TYPE,    "Dock"),
                             (SECURE_STATION_TYPE,  "Secure"),
                             (RETURN_STATION_TYPE,  "Return to Earth"),
                           )
    
    # Schema definition
    host            = models.CharField(max_length=HOST_FIELD_LENGTH, blank=True)
    station_type    = models.CharField(max_length=STATION_TYPE_FIELD_LENGTH, choices=STATION_TYPE_CHOICES, default=UNKNOWN_STATION_TYPE)
    station_id      = models.CharField(max_length=STATION_ID_FIELD_LENGTH, blank=True)
    serial_num      = models.CharField(max_length=SERIAL_NUM_FIELD_LENGTH, blank=True, unique=True)
    url             = models.CharField(max_length=URL_FIELD_LENGTH, blank=True)
    joined          = models.ForeignKey("PiEvent", null=True, on_delete=models.SET_NULL)
    last_activity   = models.DateTimeField(auto_now_add=True, blank=True)
    
    @staticmethod
    def allowedHost(host):
        """ Verify that the host is in STATION_IPS """
        try:
            return host in Setting.get("STATION_IPS").strip().split()
        except ObjectDoesNotExist:
            return False
        
    @staticmethod
    def allowedSerialNum(serialNum):
        """ Verify that the serialNum is in STATION_SERIAL_NUMS """
        try:
            return serialNum in Setting.get("STATION_SERIAL_NUMS").strip().split()
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
    MESSAGE_FIELD_LENGTH = 1000

    # Values for type
    UNKNOWN_TYPE                  = -1
    REGISTER_MSG_TYPE             = 1
    CHECKIN_TYPE                  = 2
    ADDORG_TYPE                   = 3
    ADDUSER_TYPE                  = 4
    ADDTEAM_TYPE                  = 5
    JOIN_MSG_TYPE                 = 6
    LEAVE_MSG_TYPE                = 7
    STATION_STATUS_MSG_TYPE       = 8
    UNREGISTER_MSG_TYPE           = 9
    AT_WAYPOINT_MSG_TYPE          = 10
    START_CHALLENGE_MSG_TYPE      = 11
    SUBMIT_MSG_TYPE               = 12
    REGISTER_2015_MSG_TYPE        = 13
    AT_WAYPOINT_2015_MSG_TYPE     = 14
    START_CHALLENGE_2015_MSG_TYPE = 15
    SUBMIT_2015_MSG_TYPE          = 16
    DOCK_MSG_TYPE                 = 17
    LATCH_MSG_TYPE                = 18
    OPEN_MSG_TYPE                 = 19
    SECURE_MSG_TYPE               = 20
    RETURN_MSG_TYPE               = 21
    EVENT_CONCLUDED_MSG_TYPE      = 22
    EVENT_STARTED_MSG_TYPE        = 23
    LOG_MESSAGE_MSG_TYPE          = 24
    RESET_MSG_TYPE                = 25
    STATION_SUBMIT_MSG_TYPE       = 26

    TYPE_CHOICES = (
                    (UNKNOWN_TYPE,                  "Unknown"),
                    (REGISTER_MSG_TYPE,             "Register"),
                    (CHECKIN_TYPE,                  "Check In"),
                    (ADDORG_TYPE,                   "Add Organization"),
                    (ADDUSER_TYPE,                  "Add User"),
                    (ADDTEAM_TYPE,                  "Add Team"),
                    (JOIN_MSG_TYPE,                 "Join"),
                    (LEAVE_MSG_TYPE,                "Leave"),
                    (STATION_STATUS_MSG_TYPE,       "Station Status"),
                    (UNREGISTER_MSG_TYPE,           "Unregister"),
                    (AT_WAYPOINT_MSG_TYPE,          "At Waypoint"),
                    (START_CHALLENGE_MSG_TYPE,      "Start Challenge"),
                    (SUBMIT_MSG_TYPE,               "Submit"),
                    (REGISTER_2015_MSG_TYPE,        "Register (2015)"),
                    (AT_WAYPOINT_2015_MSG_TYPE,     "At Waypoint (2015)"),
                    (START_CHALLENGE_2015_MSG_TYPE, "Start Challenge (2015)"),
                    (SUBMIT_2015_MSG_TYPE,          "Submit (2015)"),
                    (DOCK_MSG_TYPE,                 "Dock"),
                    (LATCH_MSG_TYPE,                "Latch"),
                    (OPEN_MSG_TYPE,                 "Open"),
                    (SECURE_MSG_TYPE,               "Secure"),
                    (RETURN_MSG_TYPE,               "Return"),
                    (EVENT_CONCLUDED_MSG_TYPE,      "Event Concluded"),
                    (EVENT_STARTED_MSG_TYPE,        "Event Started"),
                    (LOG_MESSAGE_MSG_TYPE,          "Log Message"),
                    (RESET_MSG_TYPE,                "Reset Team"),
                    (STATION_SUBMIT_MSG_TYPE,       "Station Submit"),
                   )
    
    MSG_TYPES_2015 = (REGISTER_2015_MSG_TYPE,
                      AT_WAYPOINT_2015_MSG_TYPE,
                      START_CHALLENGE_2015_MSG_TYPE,
                      SUBMIT_2015_MSG_TYPE,
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

        
