from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.utils.timezone import utc
from datetime import datetime, timedelta
import json
import logging
from dbkeeper.models import Organization, Team
from piservice.models import PiEvent, PiStation


#-------------------------------------------------------------------------------
def index(request):
    """ Display the scoreboard page. Updating is driven by the page making
        REST requests.
    """
    logging.debug('Entered scoreboard.views.index')

    refreshInterval = 20000 # TODO Setting.get("SCOREBOARD_STATUS_REFRESH_INTERVAL_MS", default="5000")

    context = {
        "PAGE_REFRESH_INTERVAL": refreshInterval
    }

    result = render(request, "scoreboard/index.html", context)

    logging.debug('Exiting scoreboard.views.index')
    return result


#-------------------------------------------------------------------------------
class ScoreboardStatus(View):

    #---------------------------------------------------------------------------
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

        now = datetime.utcnow().replace(tzinfo=utc)
        score = 0
        start_time = now

        # find all PiEvent.START_CHALLENGE_MSG_TYPE events and note timestamps
        teamEvents = PiEvent.objects.filter(
            team__name=teamName
        ).filter(
            pi__station_type=PiStation.LAUNCH_STATION_TYPE
        ).order_by('time')

        startChallengeEvents = teamEvents.filter(
            type=PiEvent.START_CHALLENGE_MSG_TYPE
        ).order_by('time')

        if startChallengeEvents.count() > 0:
            score = 1
            start_time = startChallengeEvents[0].time

        time_to_exit = False
        num_failed_attempts = 0
        i = 0

        while not time_to_exit:
            attemptNum = i + 1
            logging.debug('Not yet time to exit; processing attempt {} of {} for team {}'.format(attemptNum, startChallengeEvents.count(), teamName))

            if i < startChallengeEvents.count():
                logging.debug('Examining more START_CHALLENGE events')
                # need to get range t..u of events for this attempt only

                t = startChallengeEvents[i].time # timestamp of next START_CHALLENGE event

                if attemptNum < startChallengeEvents.count():
                    logging.debug('More attempts for team follow')
                    u = startChallengeEvents[attemptNum].time # timestamp of following event
                else:
                    logging.debug('No more attempts for team or event concluded')
                    gameOverEvents = PiEvent.objects.filter(
                        type=PiEvent.EVENT_CONCLUDED_MSG_TYPE
                    ).order_by('time')

                    if gameOverEvents.count() > 0:
                        logging.debug('Detected game over - event concluded')
                        u = gameOverEvents[0].time
                    else:
                        logging.debug('No more attempts for team')
                        u = teamEvents.reverse()[0].time # get last event timestamp

                logging.debug('Processing events for Team "{}" attempt #{} from {}..{}'.format(teamName, attemptNum, t, u))

                # get events within t..u range with status SUCCESS_STATUS or FAIL_STATUS
                submitEvents = teamEvents.filter(
                    type=PiEvent.SUBMIT_MSG_TYPE
                ).filter(
                    (Q(status=PiEvent.SUCCESS_STATUS) | Q(status=PiEvent.FAIL_STATUS)),
                    Q(time__gte=t),
                    Q(time__lte=u)
                )

                num_success_events = submitEvents.filter(
                    status=PiEvent.SUCCESS_STATUS
                ).count()

                num_fail_events = submitEvents.filter(
                    status=PiEvent.FAIL_STATUS
                ).count()

                cur_attempt_score = (2 * num_success_events) + (1 * num_fail_events)

                if submitEvents.count() < 4:
                    logging.debug('Getting events within t..u range with EVENT_CONCLUDED_MSG_TYPE')

                    events = teamEvents.filter(
                        type=PiEvent.EVENT_CONCLUDED_MSG_TYPE
                    ).filter(
                        Q(time__gte=t),
                        Q(time__lte=u)
                    )

                    if events.count() > 0:
                        score = cur_attempt_score
                        time_to_exit = true
                        end_time = events[0].time
                    else:
                        logging.debug('Phone probably died and need to start over, or challenge still in-progress')
                        pass
                else:
                    if submitEvents.count() > 4:
                        logging.error('More than four SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attemptNum, teamName, t, u))

                    score = cur_attempt_score
                    time_to_exit = true
                    end_time = submitEvents.reverse()[0].time # timestamp of final SUCCESS_STATUS or FAIL_STATUS event

                ++i
            else:
                logging.debug('Challenge still in-progress')
                time_to_exit = True
                end_time = now

        duration_s = (end_time - start_time).total_seconds()

        logging.debug('Exiting ScoreboardStatus._recomputeLaunchScore')
        return (score, duration_s)


    #---------------------------------------------------------------------------
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


    #---------------------------------------------------------------------------
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


    #---------------------------------------------------------------------------
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


    #---------------------------------------------------------------------------
    @staticmethod
    def _recomputeTeamScore(teamName):
        logging.debug('Entered ScoreboardStatus._recomputeTeamScore')

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

        logging.debug('Exiting ScoreboardStatus._recomputeTeamScore')
        return result


    #---------------------------------------------------------------------------
    """ A REST request to get scores from the database for the leaderboard """
    def get(self, request):
        """ Retrieve score information from the database and return it """
        logging.debug('Entered ScoreboardStatus.get')

        teams = Team.objects.all()
        teamList = []

        for t in teams:
            s = ScoreboardStatus._recomputeTeamScore(t.name)

            team = {
                "team_icon"      : "TODO (team_icon)",
                "team_name"      : t.name,
                "team_id"        : "TODO (team_id)",
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

        #-------------------
        # TODO Delete
        #for e in submitEvents:
        #    logging.debug('3: {} {} [type={}, team={}, pi={}] {}'.format(e.time, e.message, e.type, e.team, e.pi, e.status))
        #for e in events:
        #    logging.debug('{} [type={}, team={}, pi={}] {}'.format(e.time, e.type, e.team, e.pi, e.status))
        #for e in events:
        #    logging.debug('1: {} [type={}, team={}, pi={}] {}'.format(e.time, e.type, e.team, e.pi, e.status))
        #logging.debug('2: {} vs. {}'.format(now, start_time))
        # timestamps in e.time for e in events
        #for e in events:
        #    logging.debug('{} {} [type={}, team={}, pi={}] {}'.format(e.time, e.message, e.type, e.team, e.pi, e.status))
        # for e in events:
        #     logging.debug('{} {} [type={}, team={}, pi={}] {}'.format(e.time, e.message, e.type, e.team, e.pi, e.status))
        # logging.debug('[count={}]'.format(events.count()))
        #
        # TODO Delete
        #score = 0
        #duration_s = 0
        #-------------------

        logging.debug('Exiting ScoreboardStatus.get')
        return result


    #---------------------------------------------------------------------------
    @staticmethod
    def _formatSeconds(seconds):
        """ Convert seconds to mm:ss
        
            Args:
                seconds (int): number of seconds
            Returns:
                string containing mm:ss
        """
        return "{:02d}:{:02d}".format(int(seconds/60), int(seconds)%60)

