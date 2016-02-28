from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.utils.timezone import utc
from datetime import datetime, timedelta
import json
import logging
import os
from dbkeeper.models import Organization, Team, Setting
from PIL import Image, ImageDraw, ImageFont
from piservice.models import PiEvent, PiStation
from random import randint


# TODO Update doc comments throughout file
#-------------------------------------------------------------------------------
def index(request):
    """ Display the scoreboard page. Updating is driven by the page making
        REST requests.
    """
    logging.debug('Entered scoreboard.views.index')

    refreshInterval_ms = ScoreboardStatus.getSetting('SCOREBOARD_STATUS_REFRESH_INTERVAL_MS', 5000)

    context = {
        "PAGE_REFRESH_INTERVAL": refreshInterval_ms
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
        pass


    #---------------------------------------------------------------------------
    @staticmethod
    def getSetting(key,
                   ridiculous_default):
        result = Setting.get(key, ridiculous_default)

        if result == ridiculous_default:
            logging.warning("No {} key found in the Settings table. Proceeding with value {}".format(key, ridiculous_default))

        return result


    #---------------------------------------------------------------------------
    @staticmethod
    def _getEvents(team_name,
                   station_type,
                   now):
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

        return (team_events, start_challenge_events, score, start_time)


    #---------------------------------------------------------------------------
    @staticmethod
    def _getNextEventTimestamp(attempt_num,
                               start_challenge_events,
                               team_events):
        if attempt_num < start_challenge_events.count():
            logging.debug('More attempts for team follow')
            result = start_challenge_events[attempt_num].time # timestamp of following event
        else:
            logging.debug('No more attempts for team or event concluded')
            game_over_events = PiEvent.objects.filter(
                type=PiEvent.EVENT_CONCLUDED_MSG_TYPE
            ).order_by('time')

            if game_over_events.count() > 0:
                logging.debug('Detected game over - event concluded')
                result = game_over_events[0].time
            else:
                logging.debug('No more attempts for team')
                result = team_events.reverse()[0].time # get last event timestamp

        return result

    #---------------------------------------------------------------------------
    @staticmethod
    def _computeLaunch(team_name,
                       attempt_num,
                       max_submit_events,
                       params,
                       now):
        logging.debug('Entered ScoreboardStatus._computeLaunch({})'.format(team_name))

        if params['submit_events'].count() > max_submit_events:
            logging.error('More than four SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attempt_num, team_name, params['t'], params['u']))

        params['score'] = params['cur_attempt_score']
        params['time_to_exit'] = True
        params['end_time'] = params['submit_events'].reverse()[0].time # timestamp of final SUCCESS_STATUS or FAIL_STATUS event

        logging.debug('Exiting ScoreboardStatus._computeLaunch')


    #---------------------------------------------------------------------------
    @staticmethod
    def _getDataField(submit_message,
                      json_field_name):

        data = json.loads(submit_message.data)
        result = data[json_field_name]

        return result


    #---------------------------------------------------------------------------
    @staticmethod
    def _computeRunningTimeDelta(submit_message):
        dock_sim_playback_time_s = ScoreboardStatus.getSetting('DOCK_SIM_PLAYBACK_TIME_S', -6000)
        dnf_time_penalty_factor = ScoreboardStatus.getSetting('DNF_TIME_PENALTY_FACTOR', -8000)
        actual_time_s = _getDataField(submit_message, 'candidate_answer')
        fail_message = _getDataField(submit_message, 'fail_message')

        # Time charged for the actual docking flight maneuver
        if fail_message == "OUTCOME_DNF":
            flying_time_s = actual_time_s * dnf_time_penalty_factor
        else:
            flying_time_s = actual_time_s

        # Time watching the animation
        watching_time_s = min(flying_time_s, dock_sim_playback_time_s)

        return flying_time_s - watching_time_s


    #---------------------------------------------------------------------------
    @staticmethod
    def _computeDock(team_name,
                     attempt_num,
                     max_submit_events,
                     params,
                     now):
        logging.debug('Entered ScoreboardStatus._computeDock({})'.format(team_name))

        num_success_events = params['success_events'].count()
        num_fail_events = params['fail_events'].count()

        if params['latch_events'].count() > 0:
            latch_event_timestamp = params['latch_events'].reverse()[0].time # timestamp of final LATCH
        else:
            # team hasn't scanned the LATCH QR code yet 
            latch_event_timestamp = now

        if num_success_events > 0:
            if params['submit_events'].count() > max_submit_events:
                logging.error('More than one SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attempt_num, team_name, params['t'], params['u']))

            submit_message = params['submit_events'][attempt_num - 1]
            params['total_run_time_delta_s'] += ScoreboardStatus._computeRunningTimeDelta(submit_message)

            params['score'] = 9
            params['time_to_exit'] = True
            params['end_time'] = latch_event_timestamp + params['total_run_time_delta_s']

        elif num_fail_events > 0:
            if params['submit_events'].count() > max_submit_events:
                logging.error('More than one SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attempt_num, team_name, params['t'], params['u']))

            params['num_failed_attempts'] += 1

            submit_message = params['submit_events'][attempt_num - 1]
            params['total_run_time_delta_s'] += ScoreboardStatus._computeRunningTimeDelta(submit_message)

            if params['num_failed_attempts'] > 3:
                params['score'] = 5
                params['time_to_exit'] = True
                params['end_time'] = latch_event_timestamp + params['total_run_time_delta_s']

        else:
            logging.error('SUBMIT event encountered that is not a SUCCESS nor a FAIL status; skipping')

        logging.debug('Exiting ScoreboardStatus._computeDock')


    #---------------------------------------------------------------------------
    @staticmethod
    def _computeSecureOrReturn(team_name,
                               attempt_num,
                               max_submit_events,
                               params,
                               now):
        logging.debug('Entered ScoreboardStatus._computeSecureOrReturn({})'.format(team_name))

        num_success_events = params['success_events'].count()
        num_fail_events = params['fail_events'].count()

        if num_success_events > 0:
            if params['submit_events'].count() > max_submit_events:
                logging.error('More than one SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attempt_num, team_name, params['t'], params['u']))

            params['score'] = 9
            params['time_to_exit'] = True
            params['end_time'] = params['success_events'].reverse()[0].time # timestamp of final SUCCESS_STATUS

        elif num_fail_events > 0:
            if params['submit_events'].count() > max_submit_events:
                logging.error('More than one SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attempt_num, team_name, params['t'], params['u']))

            params['num_failed_attempts'] += 1

            if params['num_failed_attempts'] > 3:
                params['score'] = 5
                params['time_to_exit'] = True
                params['end_time'] = params['fail_events'].reverse()[0].time # timestamp of final FAIL_STATUS

        else:
            logging.error('SUBMIT event encountered that is not a SUCCESS nor a FAIL status; skipping')

        logging.debug('Exiting ScoreboardStatus._computeSecureOrReturn')


    #---------------------------------------------------------------------------
    @staticmethod
    def _recomputeScore(algorithm,
                        team_name,
                        station_type,
                        max_submit_events,
                        calc_current_attempt_score,
                        now):
        (team_events, start_challenge_events, score, start_time) = ScoreboardStatus._getEvents(team_name, station_type, now)

        params = {}
        params['score'] = score
        params['time_to_exit'] = False
        params['num_failed_attempts'] = 0
        params['current_run_time'] = 0
        params['docking_time_s'] = 0
        params['total_run_time_delta_s'] = 0.0
        params['latch_events'] = team_events.filter(
            type=PiEvent.LATCH_MSG_TYPE
        ).order_by('time')

        i = 0

        while not params['time_to_exit']:
            attempt_num = i + 1
            #logging.debug('Not yet time to exit; processing attempt {} of {} for team {}'.format(attempt_num, start_challenge_events.count(), team_name))

            if i < start_challenge_events.count():
                logging.debug('Examining more START_CHALLENGE events')
                # need to get range t..u of events for this attempt only

                params['t'] = start_challenge_events[i].time # timestamp of next START_CHALLENGE event
                params['u'] = ScoreboardStatus._getNextEventTimestamp(attempt_num, start_challenge_events, team_events)

                logging.debug('Processing events for Team "{}" attempt #{} from {}..{}'.format(team_name, attempt_num, params['t'], params['u']))

                # get events within t..u range with status SUCCESS_STATUS or FAIL_STATUS
                params['submit_events'] = team_events.filter(
                    type=PiEvent.SUBMIT_MSG_TYPE
                ).filter(
                    (Q(status=PiEvent.SUCCESS_STATUS) | Q(status=PiEvent.FAIL_STATUS)),
                    Q(time__gte=params['t']),
                    Q(time__lte=params['u'])
                )

                params['success_events'] = params['submit_events'].filter(
                    status=PiEvent.SUCCESS_STATUS
                )

                params['fail_events'] = params['submit_events'].filter(
                    status=PiEvent.FAIL_STATUS
                )

                num_success_events = params['success_events'].count()
                num_fail_events = params['fail_events'].count()

                params['cur_attempt_score'] = 5

                if calc_current_attempt_score:
                    params['cur_attempt_score'] = (2 * num_success_events) + (1 * num_fail_events)

                if params['submit_events'].count() < max_submit_events:
                    logging.debug('Getting events within t..u range with EVENT_CONCLUDED_MSG_TYPE')

                    events = team_events.filter(
                        type=PiEvent.EVENT_CONCLUDED_MSG_TYPE
                    ).filter(
                        Q(time__gte=params['t']),
                        Q(time__lte=params['u'])
                    )

                    if events.count() > 0:
                        params['score'] = params['cur_attempt_score']
                        params['time_to_exit'] = True
                        params['end_time'] = events[0].time
                    else:
                        logging.debug('Phone probably died and need to start over, or challenge still in-progress')
                else:
                    algorithm(team_name,
                              attempt_num,
                              max_submit_events,
                              params,
                              now)

                i += 1
            else:
                #logging.debug('Challenge complete; time to exit')
                params['time_to_exit'] = True
                params['end_time'] = now

        duration_s = (params['end_time'] - start_time).total_seconds() + params['docking_time_s']

        return (params['score'], duration_s)

    #---------------------------------------------------------------------------
    @staticmethod
    def _recomputeTeamScore(team_name):
        now = datetime.utcnow().replace(tzinfo=utc)

        (launch_score, launch_duration_s) = ScoreboardStatus._recomputeScore(ScoreboardStatus._computeLaunch,
                                                                             team_name,
                                                                             PiStation.LAUNCH_STATION_TYPE,
                                                                             4,
                                                                             True,
                                                                             now)
        (dock_score,   dock_duration_s)   = ScoreboardStatus._recomputeScore(ScoreboardStatus._computeDock,
                                                                             team_name,
                                                                             PiStation.DOCK_STATION_TYPE,
                                                                             1,
                                                                             False,
                                                                             now)
        (secure_score, secure_duration_s) = ScoreboardStatus._recomputeScore(ScoreboardStatus._computeSecureOrReturn,
                                                                             team_name,
                                                                             PiStation.SECURE_STATION_TYPE,
                                                                             1,
                                                                             False,
                                                                             now)
        (return_score, return_duration_s) = ScoreboardStatus._recomputeScore(ScoreboardStatus._computeSecureOrReturn,
                                                                             team_name,
                                                                             PiStation.RETURN_STATION_TYPE,
                                                                             1,
                                                                             False,
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

        return result


    #---------------------------------------------------------------------------
    """ A REST request to get scores from the database for the leaderboard """
    def get(self, request):
        """ Retrieve score information from the database and return it """

        teams = Team.objects.all()
        teamList = []

        for t in teams:
            s = ScoreboardStatus._recomputeTeamScore(t.name)

            if t.registered == None:
                registered_icon = "hourglass"
                registered_color = "yellow"
            else:
                registered_icon = "phone"
                registered_color = "#00ff40"

            launch_score = s['launch_score']
            dock_score = s['dock_score']
            secure_score = s['secure_score']
            return_score = s['return_score']
            total_score = launch_score + dock_score + secure_score + return_score

            launch_duration_s = s['launch_duration_s']
            dock_duration_s = s['dock_duration_s']
            secure_duration_s = s['secure_duration_s']
            return_duration_s = s['return_duration_s']
            total_duration_s = launch_duration_s + dock_duration_s + secure_duration_s + return_duration_s

            team = {
                "team_icon"       : "/scoreboard/team_icon/" + t.name + "/",
                "team_name"       : t.name,
                "organization"    : t.organization.name,
                "registered_icon" : registered_icon,
                "registered_color": registered_color,
                "launch_score"    : launch_score,
                "launch_duration" : ScoreboardStatus._formatSeconds(launch_duration_s),
                "dock_score"      : dock_score,
                "dock_duration"   : ScoreboardStatus._formatSeconds(dock_duration_s),
                "secure_score"    : secure_score,
                "secure_duration" : ScoreboardStatus._formatSeconds(secure_duration_s),
                "return_score"    : return_score,
                "return_duration" : ScoreboardStatus._formatSeconds(return_duration_s),
                "total_score"     : total_score,
                "total_duration"  : ScoreboardStatus._formatSeconds(total_duration_s),
            }

            teamList.append(team)

        result = HttpResponse(json.dumps(teamList), content_type="application/json", status=200)

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


#-------------------------------------------------------------------------------
class TeamIcon(View):

    #---------------------------------------------------------------------------
    """ A class-based view to handle a Team Icon Ajax request.
    
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
        logging.debug('Entered TeamIcon.__init__')


    #---------------------------------------------------------------------------
    """ TODO A REST request to get scores from the database for the leaderboard """
    def get(self, request, team_name):
        """ TODO Retrieve score information from the database and return it """
        logging.debug('Entered TeamIcon.get(' + team_name + ')')

        team_initial = team_name[0]
        text = team_initial.upper()

        colors = [
            {'polygon': (0xbc, 0xd2, 0xc8), 'text': (0x00, 0x00, 0x00)},
            {'polygon': (0xf6, 0xf4, 0xf1), 'text': (0x00, 0x00, 0x00)},
            {'polygon': (0xd9, 0xa0, 0x95), 'text': (0x00, 0x00, 0x00)},
            {'polygon': (0xa3, 0x61, 0x67), 'text': (0x00, 0x00, 0x00)},
            {'polygon': (0x48, 0x44, 0x52), 'text': (0xf8, 0xf2, 0xda)},
            {'polygon': (0xf8, 0xf2, 0xda), 'text': (0x00, 0x00, 0x00)},
            {'polygon': (0xc7, 0xaf, 0xbd), 'text': (0x00, 0x00, 0x00)},
            {'polygon': (0xdd, 0xec, 0xef), 'text': (0x00, 0x00, 0x00)},
        ]

        color = colors[randint(0, len(colors)-1)]

        img_width = 32
        img_height = 32

        img = Image.new("RGBA", (img_width, img_height), (255, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.ellipse((0, 0, img_width-1, img_height-1), fill=color['polygon'])

        try:
            font_size = 24

            fonts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/scoreboard/fonts')
            font = ImageFont.truetype(os.path.join(fonts_path, 'EnchantedPrairieDog.TTF'), font_size)
            (text_width, text_height) = draw.textsize(text, font=font)

            x = (img_width - text_width) / 2
            y = 0
            draw.text((x, y), text, font=font, fill=color['text'])
        except Exception, e:
            logging.warning('Error drawing text on image: {}'.format(e))

        result = HttpResponse(content_type="image/png", status=200)
        img.save(result, "PNG")

        logging.debug('Exiting TeamIcon.get')
        return result
