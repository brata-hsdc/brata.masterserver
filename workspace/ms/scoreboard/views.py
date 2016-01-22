from django.shortcuts import render, HttpResponse
from django.views.generic import View
import json
import logging
from dbkeeper.models import Organization, Team
from piservice.models import PiEvent, PiStation


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


    @staticmethod
    def _recomputeLaunchScore(teamName):
        logging.debug('Entered ScoreboardStatus._recomputeLaunchScore({})'.format(teamName))

        events = PiEvent.objects.filter(
            team__name=teamName
        ).filter(
            pi__station_type=PiStation.LAUNCH_STATION_TYPE
        )

        # TODO - Pull from issue Detailed Design



        # TODO Delete
        #for e in events:
        #    logging.debug('{} [type={}, team={}, pi={}] {}'.format(e.time, e.type, e.team, e.pi, e.status))

        # TODO Delete
        score = 0
        duration_s = 0

        logging.debug('Exiting ScoreboardStatus._recomputeLaunchScore')
        return (score, duration_s)


    @staticmethod
    def _recomputeDockScore(teamName):
        logging.debug('Entered ScoreboardStatus._recomputeDockScore({})'.format(teamName))

        events = PiEvent.objects.filter(
            team__name=teamName
        ).filter(
            pi__station_type=PiStation.DOCK_STATION_TYPE
        )

        # TODO - Pull from issue Detailed Design

        # TODO Delete
        score = 0
        duration_s = 0

        logging.debug('Exiting ScoreboardStatus._recomputeDockScore')
        return (score, duration_s)


    @staticmethod
    def _recomputeSecureScore(teamName):
        logging.debug('Entered ScoreboardStatus._recomputeSecureScore({})'.format(teamName))

        events = PiEvent.objects.filter(
            team__name=teamName
        ).filter(
            pi__station_type=PiStation.SECURE_STATION_TYPE
        )

        # TODO - Pull from issue Detailed Design

        # TODO Delete
        score = 0
        duration_s = 0

        logging.debug('Exiting ScoreboardStatus._recomputeSecureScore')
        return (score, duration_s)


    @staticmethod
    def _recomputeReturnScore(teamName):
        logging.debug('Entered ScoreboardStatus._recomputeReturnScore({})'.format(teamName))

        events = PiEvent.objects.filter(
            team__name=teamName
        ).filter(
            pi__station_type=PiStation.RETURN_STATION_TYPE
        )

        # TODO - Pull from issue Detailed Design

        # TODO Delete
        score = 0
        duration_s = 0

        logging.debug('Exiting ScoreboardStatus._recomputeReturnScore')
        return (score, duration_s)


    @staticmethod
    def _recomputeTeamScore(teamName):
        logging.debug('Entered ScoreboardStatus._recomputeScores')

        (launch_score, launch_duration_s) = ScoreboardStatus._recomputeLaunchScore(teamName)
        (dock_score,   dock_duration_s)   = ScoreboardStatus._recomputeDockScore(teamName)
        (secure_score, secure_duration_s) = ScoreboardStatus._recomputeSecureScore(teamName)
        (return_score, return_duration_s) = ScoreboardStatus._recomputeReturnScore(teamName)

        total_score = launch_score + dock_score + secure_score + return_score
        total_duration_s = launch_duration_s + dock_duration_s + secure_duration_s + return_duration_s

        result = dict(
            launch_score=launch_score,
            launch_duration_s=launch_duration_s,
            dock_score=dock_score,
            dock_duration_s=dock_duration_s,
            secure_score=secure_score,
            secure_duration_s=secure_duration_s,
            return_score=return_score,
            return_duration_s=return_duration_s,
            total_score=total_score,
            total_duration_s=total_duration_s
        )

        logging.debug('Exiting ScoreboardStatus._recomputeScores')
        return result


    """ A REST request to get scores from the database for the leaderboard """
    def get(self, request):
        """ Retrieve score information from the database and return it """
        logging.debug('Entered ScoreboardStatus.get')

        # TODO move this out of here; should this be run via cron somehow? We don't
        # want the scoreboard web page driving scoring computation--just display
        # precomputed scores.
        Scores._recomputeScores()

        teams = Team.objects.all()
        teamList = []

        for t in teams:
            s = ScoreboardStatus._recomputeTeamScore(t.name)

            team = {
                "team_icon"      : "TODO", 
                "team_name"      : t.name,
                "team_id"        : "TODO",
                "organization"   : t.organization.name,
                "is_registered"  : t.registered,
                "launch_score"   : s['launch_score'],
                "launch_duration": ScoreboardStatus._formatSeconds(s['launch_duration_s']),
                "dock_score"     : s['dock_score'],
                "dock_duration"  : ScoreboardStatus._formatSeconds(s['dock_duration_s']),
                "secure_score"   : s['secure_score'],
                "secure_duration": ScoreboardStatus._formatSeconds(s['secure_duration_s']),
                "return_score"   : s['return_score'],
                "return_duration": ScoreboardStatus._formatSeconds(s['return_duration_s']),
                "total_score"    : 0, #TODO t.total_score,
                "total_duration" : 0, #TODO ScoreboardStatus._formatSeconds(t.total_duration_s),
            }

            teamList.append(team)

        result = HttpResponse(json.dumps(teamList), content_type="application/json", status=200)

        logging.debug('Exiting ScoreboardStatus.get')
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

