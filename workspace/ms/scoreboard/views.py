from django.shortcuts import render, HttpResponse
from django.views.generic import View
import json
import logging
from dbkeeper.models import Organization, Team
from piservice.models import PiEvent, PiStation


#TODO
##----------------------------------------------------------------------------
#class Scoreboard(View):
#    """ Display the scoreboard page.
#        Updating is driven by the page making REST requests.
#    """
#    context = {}
#    def get(self, request):
#        return render(request, "scoreboard/scoreboard.html", self.context)
#
##----------------------------------------------------------------------------
#class Scores(View):
#    """ A REST request to get scores from the database for the leaderboard """
#    def get(self, request):
#        """ Retrieve score information from the database and return it """
#        # Get scores from the database
#        # Format scores into JSON
#        # Return
#        return HttpResponse("")


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
        logging.debug('Entered Scores.__init__')


    @staticmethod
    def _recomputeLaunchScore(teamName):
        logging.debug('Entered Scores._recomputeLaunchScore({})'.format(teamName))

        events = PiEvent.objects.filter(
            team__name=teamName
        ).filter(
            pi__station_type=PiStation.LAUNCH_STATION_TYPE
        )

        # PDL:
        # score = 0
        # find all PiEvent.START_CHALLENGE_MSG_TYPE events and note timestamps
        # if any found then
        #     score = 1
        #     start_time = timestamp of 1st event
        # end if
        #
        # time_to_exit = false
        # num_failed_attempts = 0
        #
        # while not time_to_exit
        #     if there are more START_CHALLENGE events that we haven't looked at yet then
        #         get timestamp t of next START_CHALLENGE event
        #         get timestamp u of following START_CHALLENGE event or TODO (final design challenge has concluded event) event if it exists; o/w timestamp u of last event
        #
        #         if there are four events within t..u range with status SUCCESS_STATUS or FAIL_STATUS then
        #             score = 2 * num SUCCESS events + 1 * num FAIL events
        #             time_to_exit = true
        #             end_time = timestamp of final SUCCESS_STATUS or FAIL_STATUS event
        #         else if there is an event within t..u range with TODO (final design challenge has concluded event) then
        #             score = 2 * num SUCCESS events + 1 * num FAIL events
        #             time_to_exit = true
        #             end_time = timestamp of TODO (final design challenge has concluded event) event
        #         else
        #             # phone probably died and need to start over, or challenge
        #             # still in-progress
        #             pass
        #         end if
        #     else
        #         # challenge still in-progress
        #         time_to_exit = true
        #         end_time = current time
        #     end if
        # end while
        #
        # duration_s = end_time - start_time





        # TODO Delete
        #for e in events:
        #    logging.debug('{} [type={}, team={}, pi={}] {}'.format(e.time, e.type, e.team, e.pi, e.status))

        # TODO Delete
        score = 0
        duration_s = 0

        logging.debug('Exiting Scores._recomputeLaunchScore')
        return (score, duration_s)


    @staticmethod
    def _recomputeDockScore(teamName):
        logging.debug('Entered Scores._recomputeDockScore({})'.format(teamName))

        events = PiEvent.objects.filter(
            team__name=teamName
        ).filter(
            pi__station_type=PiStation.DOCK_STATION_TYPE
        )

        # Assumptions:
        #     * One SUCCESS/FAIL event will be posted after the user scans the Secure QR code
        #     * A FAIL event is posted when each of three challenge attempts fails
        #     * The SUCCESS/FAIL events provide the actual docking time for the attempt (disregarding the simulation run time)
        #     * The 2x velocity-dropped-to-zero penalty is already accounted for in the actual docking time in the FAIL messages
        # PDL:
        # score = 0
        # find all PiEvent.START_CHALLENGE_MSG_TYPE events and note timestamps
        # if any found then
        #     score = 1
        #     start_time = timestamp of 1st event
        # end if
        #
        # time_to_exit = false
        # num_failed_attempts = 0
        #
        # while not time_to_exit
        #     if there are more START_CHALLENGE events that we haven't looked at yet then
        #         get timestamp t of next START_CHALLENGE event
        #         get timestamp u of following START_CHALLENGE event or TODO (final design challenge has concluded event) event if it exists; o/w timestamp u of last event
        #
        #         if there is an event within t..u range with status SUCCESS_STATUS then
        #             score = 9
        #             time_to_exit = true
        #             end_time = timestamp of SUCCESS_STATUS event + total actual docking time for all attempts
        #         else if there is an event within t..u range with status FAIL_STATUS then
        #             increment num_failed_attempts
        #
        #             if num_failed_attempts > 3 then
        #                 score = 5
        #                 time_to_exit = true
        #                 end_time = timestamp of FAIL_STATUS event + total actual docking time for all attempts
        #             end if
        #         else if there is an event within t..u range with TODO (final design challenge has concluded event) then
        #             score = 5
        #             time_to_exit = true
        #             end_time = timestamp of TODO (final design challenge has concluded event) event + total actual docking time for all attempts
        #         else
        #             # phone probably died and need to start over, or challenge
        #             # still in-progress
        #             pass
        #         end if
        #     else
        #         # challenge still in-progress
        #         time_to_exit = true
        #         end_time = current time
        #     end if
        # end while
        #
        # duration_s = end_time - start_time

        # TODO Delete
        score = 0
        duration_s = 0

        logging.debug('Exiting Scores._recomputeDockScore')
        return (score, duration_s)


    @staticmethod
    def _recomputeSecureScore(teamName):
        logging.debug('Entered Scores._recomputeSecureScore({})'.format(teamName))

        events = PiEvent.objects.filter(
            team__name=teamName
        ).filter(
            pi__station_type=PiStation.SECURE_STATION_TYPE
        )

        # Assumptions:
        #     * One SUCCESS/FAIL event will be posted after the user scans the Secure QR code
        #     * A FAIL event is posted when each of three challenge attempts fails
        #     * A FAIL event is _not_ posted for each incorrect response within an attempt
        # PDL:
        # score = 0
        # find all PiEvent.START_CHALLENGE_MSG_TYPE events and note timestamps
        # if any found then
        #     score = 1
        #     start_time = timestamp of 1st event
        # end if
        #
        # time_to_exit = false
        # num_failed_attempts = 0
        #
        # while not time_to_exit
        #     if there are more START_CHALLENGE events that we haven't looked at yet then
        #         get timestamp t of next START_CHALLENGE event
        #         get timestamp u of following START_CHALLENGE event or TODO (final design challenge has concluded event) event if it exists; o/w timestamp u of last event
        #
        #         if there is an event within t..u range with status SUCCESS_STATUS then
        #             score = 9
        #             time_to_exit = true
        #             end_time = timestamp of SUCCESS_STATUS event
        #         else if there is an event within t..u range with status FAIL_STATUS then
        #             increment num_failed_attempts
        #
        #             if num_failed_attempts > 3 then
        #                 score = 5
        #                 time_to_exit = true
        #                 end_time = timestamp of FAIL_STATUS event
        #             end if
        #         else if there is an event within t..u range with TODO (final design challenge has concluded event) then
        #             score = 5
        #             time_to_exit = true
        #             end_time = timestamp of TODO (final design challenge has concluded event) event
        #         else
        #             # phone probably died and need to start over, or challenge
        #             # still in-progress
        #             pass
        #         end if
        #     else
        #         # challenge still in-progress
        #         time_to_exit = true
        #         end_time = current time
        #     end if
        # end while
        #
        # duration_s = end_time - start_time

        # TODO Delete
        score = 0
        duration_s = 0

        logging.debug('Exiting Scores._recomputeSecureScore')
        return (score, duration_s)


    @staticmethod
    def _recomputeReturnScore(teamName):
        logging.debug('Entered Scores._recomputeReturnScore({})'.format(teamName))

        events = PiEvent.objects.filter(
            team__name=teamName
        ).filter(
            pi__station_type=PiStation.RETURN_STATION_TYPE
        )

        # TODO - same logic as Secure

        # TODO Delete
        score = 0
        duration_s = 0

        logging.debug('Exiting Scores._recomputeReturnScore')
        return (score, duration_s)


    @staticmethod
    def _recomputeTeamScore(teamName):
        logging.debug('Entered Scores._recomputeScores')

        (launch_score, launch_duration_s) = Scores._recomputeLaunchScore(teamName)
        (dock_score,   dock_duration_s)   = Scores._recomputeDockScore(teamName)
        (secure_score, secure_duration_s) = Scores._recomputeSecureScore(teamName)
        (return_score, return_duration_s) = Scores._recomputeReturnScore(teamName)

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

        logging.debug('Exiting Scores._recomputeScores')
        return result


    """ A REST request to get scores from the database for the leaderboard """
    def get(self, request):
        """ Retrieve score information from the database and return it """
        logging.debug('Entered ScoreboardStatus.get')

        teams = Team.objects.all()
        teamList = []

        for t in teams:
            s = ScoreboardStatus._recomputeTeamScore(t.name)

            team = {
                "team_icon"     : "TODO", 
                "team_name"     : t.name,
                "team_id"       : "TODO",
                "organization"  : t.organization.name,
                "is_registered" : t.registered,
                "launch_score"   : s['launch_score'],
                "launch_duration": Scores._formatSeconds(s['launch_duration_s']),
                "dock_score"     : s['dock_score'],
                "dock_duration"  : Scores._formatSeconds(s['dock_duration_s']),
                "secure_score"   : s['secure_score'],
                "secure_duration": Scores._formatSeconds(s['secure_duration_s']),
                "return_score"   : s['return_score'],
                "return_duration": Scores._formatSeconds(s['return_duration_s']),
                "total_score"   : t.total_score,
                "total_duration": Scores._formatSeconds(t.total_duration_s),
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
