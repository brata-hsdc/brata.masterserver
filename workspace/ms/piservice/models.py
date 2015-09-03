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
    A_PI_TYPE       = 1
    B_PI_TYPE       = 2
    BPLUS_PI_TYPE   = 3
    # TODO: add other types as appropriate
    PI_TYPE_CHOICES = (
                        (UNKNOWN_PI_TYPE, "Unknown"),
                        (A_PI_TYPE,       "Model A"),
                        (B_PI_TYPE,       "Model B"),
                        (BPLUS_PI_TYPE,   "Model B+"),
                      )
    
    # Schema definition
    host            = models.CharField(max_length=HOST_FIELD_LENGTH)
    stationType     = models.PositiveSmallIntegerField(choices=STATION_TYPE_CHOICES, default=UNKNOWN_STATION_TYPE)
    piType          = models.PositiveSmallIntegerField(choices=PI_TYPE_CHOICES, default=UNKNOWN_PI_TYPE)
    stationInstance = models.PositiveSmallIntegerField(default=0)
    
#----------------------------------------------------------------------------
class PiEvent(models.Model):
    """ A time-stamped instance of a specific occurrence, what kind of
        occurrence it was, who did it, and possibly a reference to some
        other data.
    """
    # Constants
    DATA_FIELD_LENGTH = 2000
    # Values for type
    UNKNOWN_TYPE = 0
    # TODO: add other types as appropriate
    TYPE_CHOICES = (
                    (UNKNOWN_TYPE, "Unknown"),
                   )
    
    # Schema definition
    time   = models.TimeField()
    type   = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=UNKNOWN_TYPE)
    teamID = models.ForeignKey(Team)
    piID   = models.ForeignKey(PiStation)

    # TODO: The data field could potentially be large if we start shoving
    # big JSON objects into it.  Should it be part of this table or
    # should it be a separate table that this one has a ForeignKey to?
    # I think modern RDBMS's don't store the full field size for every
    # record for char fields.  Am I wrong?
    data = models.TextField(blank=True)
    