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


    #---------------------------------------------------------------------------
    @staticmethod
    def _getEvents(team_name,
                   event_type,
                   now):
        logging.debug('Entered ScoreboardStatus._getEvents({})'.format(team_name))

        team_events = PiEvent.objects.filter(
            team__name=team_name
        ).filter(
            pi__station_type=station_type
        ).order_by('time')

        start_challenge_events = team_events.filter(
            type=PiEvent.START_CHALLENGE_MSG_TYPE
        ).order_by('time')

        score = 0
        start_time = now

        if start_challenge_events.count() > 0:
            score = 1
            start_time = start_challenge_events[0].time

        logging.debug('Exiting ScoreboardStatus._getEvents()')
        return (team_events, start_challenge_events, score, start_time)


    #---------------------------------------------------------------------------
    @staticmethod
    def _recomputeLaunchScore(team_name,
                              station_type,
                              max_submit_events,
                              now):
        logging.debug('Entered ScoreboardStatus._recomputeLaunchScore({})'.format(team_name))

#--- BEGIN COMMON
        (team_events, start_challenge_events, score, start_time) = _getEvents(team_name, station_type, now)

        time_to_exit = False
        num_failed_attempts = 0 # TODO unused
        i = 0

        while not time_to_exit:
            attemptNum = i + 1
            logging.debug('Not yet time to exit; processing attempt {} of {} for team {}'.format(attemptNum, start_challenge_events.count(), team_name))

            if i < start_challenge_events.count():
                logging.debug('Examining more START_CHALLENGE events')
                # need to get range t..u of events for this attempt only

                t = start_challenge_events[i].time # timestamp of next START_CHALLENGE event

                if attemptNum < start_challenge_events.count():
                    logging.debug('More attempts for team follow')
                    u = start_challenge_events[attemptNum].time # timestamp of following event
                else:
                    logging.debug('No more attempts for team or event concluded')
                    game_over_events = PiEvent.objects.filter(
                        type=PiEvent.EVENT_CONCLUDED_MSG_TYPE
                    ).order_by('time')

                    if game_over_events.count() > 0:
                        logging.debug('Detected game over - event concluded')
                        u = game_over_events[0].time
                    else:
                        logging.debug('No more attempts for team')
                        u = team_events.reverse()[0].time # get last event timestamp

                logging.debug('Processing events for Team "{}" attempt #{} from {}..{}'.format(team_name, attemptNum, t, u))

                # get events within t..u range with status SUCCESS_STATUS or FAIL_STATUS
                submit_events = team_events.filter(
                    type=PiEvent.SUBMIT_MSG_TYPE
                ).filter(
                    (Q(status=PiEvent.SUCCESS_STATUS) | Q(status=PiEvent.FAIL_STATUS)),
                    Q(time__gte=t),
                    Q(time__lte=u)
                )

                success_events = submit_events.filter(
                    status=PiEvent.SUCCESS_STATUS
                )

                fail_events = submit_events.filter(
                    status=PiEvent.FAIL_STATUS
                )

                num_success_events = success_events.count()
                num_fail_events = fail_events.count()
#--- END COMMON

                cur_attempt_score = (2 * num_success_events) + (1 * num_fail_events)

#--- BEGIN COMMON
                if submit_events.count() < max_submit_events:
                    logging.debug('Getting events within t..u range with EVENT_CONCLUDED_MSG_TYPE')

                    events = team_events.filter(
                        type=PiEvent.EVENT_CONCLUDED_MSG_TYPE
                    ).filter(
                        Q(time__gte=t),
                        Q(time__lte=u)
                    )

                    if events.count() > 0:
                        score = cur_attempt_score
                        time_to_exit = true
#--- END COMMON
                        end_time = events[0].time
#--- BEGIN COMMON
                    else:
                        logging.debug('Phone probably died and need to start over, or challenge still in-progress')
#--- END COMMON

                else:
                    if submit_events.count() > max_submit_events:
                        logging.error('More than four SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attemptNum, team_name, t, u))

                    score = cur_attempt_score
                    time_to_exit = true
                    end_time = submit_events.reverse()[0].time # timestamp of final SUCCESS_STATUS or FAIL_STATUS event

#--- BEGIN COMMON
                i += 1
            else:
                logging.debug('Challenge complete; time to exit')
                time_to_exit = True
                end_time = now

        duration_s = (end_time - start_time).total_seconds()
#--- END COMMON

        logging.debug('Exiting ScoreboardStatus._recomputeLaunchScore: score={}, duration={} s'.format(score, duration_s))
        return (score, duration_s)


    #---------------------------------------------------------------------------
    @staticmethod
    def _recomputeDockScore(team_name,
                            station_type,
                            max_submit_events,
                            now):
        logging.debug('Entered ScoreboardStatus._recomputeDockScore({})'.format(team_name))

#--- TODO BEGIN COMMON
        (team_events, start_challenge_events, score, start_time) = _getEvents(team_name, station_type, now)

        time_to_exit = False
        num_failed_attempts = 0
        i = 0
#--- TODO END COMMON

#--- TODO BEGIN DOCK
        current_run_time = 0
#--- TODO END DOCK

#--- TODO BEGIN COMMON
        while not time_to_exit:
            attemptNum = i + 1
            logging.debug('Not yet time to exit; processing attempt {} of {} for team {}'.format(attemptNum, start_challenge_events.count(), team_name))

            if i < start_challenge_events.count():
                logging.debug('Examining more START_CHALLENGE events')
                # need to get range t..u of events for this attempt only

                t = start_challenge_events[i].time # timestamp of next START_CHALLENGE event

                if attemptNum < start_challenge_events.count():
                    logging.debug('More attempts for team follow')
                    u = start_challenge_events[attemptNum].time # timestamp of following event
                else:
                    logging.debug('No more attempts for team or event concluded')
                    game_over_events = PiEvent.objects.filter(
                        type=PiEvent.EVENT_CONCLUDED_MSG_TYPE
                    ).order_by('time')

                    if game_over_events.count() > 0:
                        logging.debug('Detected game over - event concluded')
                        u = game_over_events[0].time
                    else:
                        logging.debug('No more attempts for team')
                        u = team_events.reverse()[0].time # get last event timestamp

                logging.debug('Processing events for Team "{}" attempt #{} from {}..{}'.format(team_name, attemptNum, t, u))

                # get events within t..u range with status SUCCESS_STATUS or FAIL_STATUS
                submit_events = team_events.filter(
                    type=PiEvent.SUBMIT_MSG_TYPE
                ).filter(
                    (Q(status=PiEvent.SUCCESS_STATUS) | Q(status=PiEvent.FAIL_STATUS)),
                    Q(time__gte=t),
                    Q(time__lte=u)
                )

                success_events = submit_events.filter(
                    status=PiEvent.SUCCESS_STATUS
                )

                fail_events = submit_events.filter(
                    status=PiEvent.FAIL_STATUS
                )

                num_success_events = success_events.count()
                num_fail_events = fail_events.count()
#--- TODO END COMMON

                cur_attempt_score = 5

#--- BEGIN COMMON
                if submit_events.count() < max_submit_events:
                    logging.debug('Getting events within t..u range with EVENT_CONCLUDED_MSG_TYPE')

                    events = team_events.filter(
                        type=PiEvent.EVENT_CONCLUDED_MSG_TYPE
                    ).filter(
                        Q(time__gte=t),
                        Q(time__lte=u)
                    )

                    if events.count() > 0:
                        score = cur_attempt_score
                        time_to_exit = true
#--- TODO END COMMON
#--- TODO BEGIN DOCK
        # TODO
        #             dnf_scale = 1.0 or value from DB depending on param in SUBMIT message
        #             attempt_run_time = timestamp of LATCH/SUBMIT event + (total actual docking time * dnf_scale)
        #             end_time = current_run_time + attempt_run_time
#--- TODO END DOCK
#--- BEGIN COMMON
                    else:
                        logging.debug('Phone probably died and need to start over, or challenge still in-progress')

                elif num_success_events > 0:
                    if submit_events.count() > max_submit_events:
                        logging.error('More than one SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attemptNum, team_name, t, u))

                    score = 9
                    time_to_exit = true
#--- TODO END COMMON
#--- TODO BEGIN DOCK
        # TODO
        #                 dnf_scale = 1.0 or value from DB depending on param in SUBMIT message
        #                 attempt_run_time = timestamp of LATCH/SUBMIT event + (total actual docking time * dnf_scale)
        #                 end_time = current_run_time + attempt_run_time
        #             else
        #                 dnf_scale = 1.0 or value from DB depending on param in SUBMIT message
        #                 attempt_run_time = timestamp of LATCH/SUBMIT event + (total actual docking time * dnf_scale)
        #                 current_run_time += attempt_run_time
#--- TODO END DOCK

#--- TODO BEGIN COMMON
                elif num_fail_events > 0:
                    if submit_events.count() > max_submit_events:
                        logging.error('More than one SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attemptNum, team_name, t, u))

                    num_failed_attempts += 1

                    if num_failed_attempts > 3:
                        score = 5
                        time_to_exit = true
#--- TODO END COMMON
#--- TODO BEGIN DOCK
        # TODO
        #             dnf_scale = 1.0 or value from DB depending on param in SUBMIT message
        #             attempt_run_time = timestamp of LATCH/SUBMIT event + (total actual docking time * dnf_scale)
        #             end_time = current_run_time + attempt_run_time
#--- TODO END DOCK

#--- TODO BEGIN COMMON
                else:
                    log.error('SUBMIT event encountered that is not a SUCCESS nor a FAIL status; skipping')

                i += 1
            else:
                logging.debug('Challenge complete; time to exit')
                time_to_exit = True
#--- TODO END COMMON
#--- TODO BEGIN DOCK
        #         TODO - Do we have a Submit message to work with here?
        #         dnf_scale = 1.0 or value from DB depending on param in SUBMIT message
        #         attempt_run_time = now + (total actual docking time * dnf_scale)
        #         end_time = current_run_time + attempt_run_time
#--- TODO END DOCK

#--- BEGIN COMMON

        duration_s = (end_time - start_time).total_seconds()
#--- END COMMON

        logging.debug('Exiting ScoreboardStatus._recomputeDockScore: score={}, duration={} s'.format(score, duration_s))
        return (score, duration_s)


    #---------------------------------------------------------------------------
    @staticmethod
    def _recomputeSecureOrReturnScore(team_name,
                                      station_type,
                                      max_submit_events,
                                      now):
        logging.debug('Entered ScoreboardStatus._recomputeSecureOrReturnScore({}, {})'.format(team_name, station_type))

#--- BEGIN COMMON
        (team_events, start_challenge_events, score, start_time) = _getEvents(team_name, station_type, now)

        time_to_exit = False
        num_failed_attempts = 0
        i = 0
#--- END COMMON

#--- BEGIN COMMON
        while not time_to_exit:
            attemptNum = i + 1
            logging.debug('Not yet time to exit; processing attempt {} of {} for team {}'.format(attemptNum, start_challenge_events.count(), team_name))

            if i < start_challenge_events.count():
                logging.debug('Examining more START_CHALLENGE events')
                # need to get range t..u of events for this attempt only

                t = start_challenge_events[i].time # timestamp of next START_CHALLENGE event

                if attemptNum < start_challenge_events.count():
                    logging.debug('More attempts for team follow')
                    u = start_challenge_events[attemptNum].time # timestamp of following event
                else:
                    logging.debug('No more attempts for team or event concluded')
                    game_over_events = PiEvent.objects.filter(
                        type=PiEvent.EVENT_CONCLUDED_MSG_TYPE
                    ).order_by('time')

                    if game_over_events.count() > 0:
                        logging.debug('Detected game over - event concluded')
                        u = game_over_events[0].time
                    else:
                        logging.debug('No more attempts for team')
                        u = team_events.reverse()[0].time # get last event timestamp

                logging.debug('Processing events for Team "{}" attempt #{} from {}..{}'.format(team_name, attemptNum, t, u))

                # get events within t..u range with status SUCCESS_STATUS or FAIL_STATUS
                submit_events = team_events.filter(
                    type=PiEvent.SUBMIT_MSG_TYPE
                ).filter(
                    (Q(status=PiEvent.SUCCESS_STATUS) | Q(status=PiEvent.FAIL_STATUS)),
                    Q(time__gte=t),
                    Q(time__lte=u)
                )

                success_events = submit_events.filter(
                    status=PiEvent.SUCCESS_STATUS
                )

                fail_events = submit_events.filter(
                    status=PiEvent.FAIL_STATUS
                )

                num_success_events = success_events.count()
                num_fail_events = fail_events.count()
#--- END COMMON

                cur_attempt_score = 5

#--- BEGIN COMMON
                if submit_events.count() < max_submit_events:
                    logging.debug('Getting events within t..u range with EVENT_CONCLUDED_MSG_TYPE')

                    events = team_events.filter(
                        type=PiEvent.EVENT_CONCLUDED_MSG_TYPE
                    ).filter(
                        Q(time__gte=t),
                        Q(time__lte=u)
                    )

                    if events.count() > 0:
                        score = cur_attempt_score
                        time_to_exit = true
#--- END COMMON
#--- BEGIN SECURE OR RETURN
                        end_time = events[0].time
#--- END SECURE OR RETURN
#--- BEGIN COMMON
                    else:
                        logging.debug('Phone probably died and need to start over, or challenge still in-progress')

#--- END COMMON

#---BEGIN SECURE OR RETURN
                elif num_success_events > 0:
                    if submit_events.count() > max_submit_events:
                        logging.error('More than one SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attemptNum, team_name, t, u))

                    score = 9
                    time_to_exit = true
                    end_time = success_events.reverse()[0].time # timestamp of final SUCCESS_STATUS

                elif num_fail_events > 0:
                    if submit_events.count() > max_submit_events:
                        logging.error('More than one SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attemptNum, team_name, t, u))

                    num_failed_attempts += 1

                    if num_failed_attempts > 3:
                        score = 5
                        time_to_exit = true
                        end_time = fail_events.reverse()[0].time # timestamp of final FAIL_STATUS

                else:
                    log.error('SUBMIT event encountered that is not a SUCCESS nor a FAIL status; skipping')
#---END SECURE OR RETURN

#--- BEGIN COMMON
                i += 1
            else:
                logging.debug('Challenge complete; time to exit')
                time_to_exit = True
#--- END COMMON
#--- BEGIN SECURE OR RETURN
                end_time = now
#--- END SECURE OR RETURN
#--- BEGIN COMMON

        duration_s = (end_time - start_time).total_seconds()
#--- END COMMON

        logging.debug('Exiting ScoreboardStatus._recomputeSecureOrReturnScore')
        return (score, duration_s)


    #---------------------------------------------------------------------------
    @staticmethod
    def _recomputeScore(algorithm,
                        team_name,
                        station_type,
                        max_submit_events,
                        now):
        logging.debug('Entered ScoreboardStatus._recomputeScore({})'.format(team_name))

        (score, duration_s) = algorithm(team_name, station_type, max_submit_events, now)

        logging.debug('Exiting ScoreboardStatus._recomputeScore()')
        return (score, duration_s)

    #---------------------------------------------------------------------------
    @staticmethod
    def _recomputeTeamScore(team_name):
        logging.debug('Entered ScoreboardStatus._recomputeTeamScore')

        now = datetime.utcnow().replace(tzinfo=utc)

        (launch_score, launch_duration_s) = ScoreboardStatus._recomputeScore(_recomputeLaunchScore,
                                                                             team_name,
                                                                             PiStation.LAUNCH_STATION_TYPE,
                                                                             4,
                                                                             now)
        (dock_score,   dock_duration_s)   = ScoreboardStatus._recomputeScore(_recomputeDockScore,
                                                                             team_name,
                                                                             PiStation.DOCK_STATION_TYPE,
                                                                             1,
                                                                             now)
        (secure_score, secure_duration_s) = ScoreboardStatus._recomputeScore(_recomputeSecureOrReturnScore,
                                                                             team_name,
                                                                             PiStation.SECURE_STATION_TYPE,
                                                                             1,
                                                                             now)
        (return_score, return_duration_s) = ScoreboardStatus._recomputeScore(_recomputeSecureOrReturnScore,
                                                                             team_name,
                                                                             PiStation.RETURN_STATION_TYPE,
                                                                             1,
                                                                             now)

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

