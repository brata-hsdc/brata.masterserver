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

    context = {
       "PAGE_REFRESH_INTERVAL": refreshInterval
    }

    result = render(request, "scoreboard/index.html", context)

    logging.debug('Exiting scoreboard.views.index')
    return result


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


    """ A REST request to get scores from the database for the leaderboard """
    def get(self, request):
        """ Retrieve score information from the database and return it """
        logging.debug('Entered ScoreboardStatus.get')
        
        teams = Team.objects.all()
        teamList = []

        for t in teams:
            team = {
                "team_icon"     : "TODO", 
                "team_name"     : t.name,
                "team_id"       : "TODO",
                "organization"  : t.organization.name,
                #"is_registered" : t.registered,
                "launch_score"   : t.launch_score,
                "launch_duration": Scores._formatSeconds(t.launch_duration_s),
                "dock_score"     : t.dock_score,
                "dock_duration"  : Scores._formatSeconds(t.dock_duration_s),
                "secure_score"   : t.secure_score,
                "secure_duration": Scores._formatSeconds(t.secure_duration_s),
                "return_score"   : t.return_score,
                "return_duration": Scores._formatSeconds(t.return_duration_s),
                "total_score"    : t.total_score,
                "total_duration" : Scores._formatSeconds(t.total_duration_s),
            }

            teamList.append(team)

        result = HttpResponse(json.dumps(teamList), content_type="application/json", status=200)

        logging.debug('Exiting Scores.get')
        return result


    @staticmethod
    def _formatSeconds(seconds):
        """ Convert seconds to mm:ss
        
            Args:
                seconds (int): number of seconds
            Returns:
                string containing mm:ss
        """
        return "{:02d}:{:02d}".format(int(seconds/60), seconds%60)
