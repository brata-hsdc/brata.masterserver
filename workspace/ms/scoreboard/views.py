from django.shortcuts import render, HttpResponse
from django.views.generic import View
import json
import logging
from dbkeeper.models import Organization, Team
from piservice.models import PiEvent


#-------------------------------------------------------------------------------
def index(request):
    """ Display the scoreboard page. Updating is driven by the page making REST requests.
    """
    logging.debug('Entered scoreboard.views.index')
    refreshInterval = 5000 # TODO Setting.get("SCOREBOARD_STATUS_REFRESH_INTERVAL_MS", default="5000")

    return render(request, "scoreboard/index.html",
                  {"PAGE_REFRESH_INTERVAL": refreshInterval})


#-------------------------------------------------------------------------------
class ScoreboardStatus(View):
    """ A class-based view to handle a Station Status Ajax request.
    
        The client sends a GET message with the following JSON data:
        {
        }
        
        The MS sends the following response on success:
        [
        	# TODO...
            {
                "host": "Second RPi Station",
                "station_id": "2:ab45",
                "joined": "2015-09-17 03:36:58",
                "type": "Unknown"
            },
            {
                "host": "First RPi Station",
                "station_id": "1:03cc",
                "joined": "",
                "type": "Unknown"
            }
        ]
    """
    def __init__(self):
        logging.debug('Entered ScoreboardStatus.__init__')

    def get(self, request, *args, **kwargs):
        """ Return the status of all the Teams """
        logging.debug('Entered ScoreboardStatus.get')
        
        #TODO        teams = Team.objects.all()
        #------------------------------------------------
        #TODO Delete
        teams = []
        s = Team()
        setattr(s, 'name', 'team1')

        org = Organization()
        setattr(org, 'name', 'org1')
        setattr(s, 'organization', org)

        #evt = PiEvent()
        #setattr(s, 'registered', evt)

        setattr(s, 'total_score', 42)
        setattr(s, 'total_duration_s', 43)
        teams.append(s)

        s = Team()
        setattr(s, 'name', 'team2')

        org = Organization()
        setattr(org, 'name', 'org2')
        setattr(s, 'organization', org)

        #evt = PiEvent()
        #setattr(s, 'registered', evt)

        setattr(s, 'total_score', 44)
        setattr(s, 'total_duration_s', 90)
        teams.append(s)

        s = Team()
        setattr(s, 'name', 'team3')

        org = Organization()
        setattr(org, 'name', 'org1')
        setattr(s, 'organization', org)

        #evt = PiEvent()
        #setattr(s, 'registered', evt)

        setattr(s, 'total_score', 46)
        setattr(s, 'total_duration_s', 3661)
        teams.append(s)
        #------------------------------------------------

        teamList = []

        for t in teams:
            team = {
                "team_icon"     : "TODO", 
                "team_name"     : t.name,
                "team_id"       : "TODO",
                "organization"  : t.organization.name,
                #"is_registered" : t.registered,
                "total_score"   : t.total_score,
                "total_duration": ScoreboardStatus._formatSeconds(t.total_duration_s),
            }

            teamList.append(team)

        logging.debug('Exiting ScoreboardStatus.get')
        return HttpResponse(json.dumps(teamList), content_type="application/json", status=200)

    @staticmethod
    def _formatSeconds(seconds):
        """ Convert seconds to mm:ss
        
            Args:
                seconds (int): number of seconds
            Returns:
                string containing mm:ss
        """
        return "{:02d}:{:02d}".format(int(seconds/60), seconds%60)
