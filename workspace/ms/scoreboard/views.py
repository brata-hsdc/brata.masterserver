from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.utils.timezone import utc
from datetime import datetime, timedelta
import json
import logging
import os
from dbkeeper.models import Organization, Team
from PIL import Image, ImageDraw, ImageFont
from piservice.models import PiEvent, PiStation
from gnome._gnome import score_init
from random import randint


#-------------------------------------------------------------------------------
def index(request):
    """ Display the scoreboard page. Updating is driven by the page making
        REST requests.
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
                   station_type,
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
    def _computeDock(team_name,
                     attempt_num,
                     max_submit_events,
                     params,
                     now):
        logging.debug('Entered ScoreboardStatus._computeDock({})'.format(team_name))

        """
#--- TODO BEGIN DOCK
TODO2:
        # TODO
        #             dnf_scale = 1.0 or value from DB depending on param in SUBMIT message
        #             attempt_run_time = timestamp of LATCH/SUBMIT event + (total actual docking time * dnf_scale)
        #             params['end_time'] = params['current_run_time'] + attempt_run_time
        params['docking_time_s'] = todo
#--- TODO END DOCK
#--- BEGIN COMMON

TODO4:
                if num_success_events > 0:
                    if params['submit_events'].count() > max_submit_events:
                        logging.error('More than one SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attempt_num, team_name, params['t'], params['u']))

                    params['score'] = 9
                    params['time_to_exit'] = True
#--- TODO END COMMON
#--- TODO BEGIN DOCK
        # TODO
        #                 dnf_scale = 1.0 or value from DB depending on param in SUBMIT message
        #                 attempt_run_time = timestamp of LATCH/SUBMIT event + (total actual docking time * dnf_scale)
        #                 params['end_time'] = params['current_run_time'] + attempt_run_time
        #             else
        #                 dnf_scale = 1.0 or value from DB depending on param in SUBMIT message
        #                 attempt_run_time = timestamp of LATCH/SUBMIT event + (total actual docking time * dnf_scale)
        #                 params['current_run_time'] += attempt_run_time
#--- TODO END DOCK

#--- TODO BEGIN COMMON
                elif num_fail_events > 0:
                    if params['submit_events'].count() > max_submit_events:
                        logging.error('More than one SUBMIT events encountered for attempt #{} by Team {} ({}..{})'.format(attempt_num, team_name, params['t'], params['u']))

                    params['num_failed_attempts'] += 1

                    if params['num_failed_attempts'] > 3:
                        params['score'] = 5
                        params['time_to_exit'] = True
#--- TODO END COMMON
#--- TODO BEGIN DOCK
        # TODO
        #             dnf_scale = 1.0 or value from DB depending on param in SUBMIT message
        #             attempt_run_time = timestamp of LATCH/SUBMIT event + (total actual docking time * dnf_scale)
        #             params['end_time'] = params['current_run_time'] + attempt_run_time
#--- TODO END DOCK

#--- TODO BEGIN COMMON
                else:
                    log.error('SUBMIT event encountered that is not a SUCCESS nor a FAIL status; skipping')

#--- TODO END COMMON
#--- TODO BEGIN DOCK
TODO3:
        #         TODO - Do we have a Submit message to work with here?
        #         dnf_scale = 1.0 or value from DB depending on param in SUBMIT message
        #         attempt_run_time = now + (total actual docking time * dnf_scale)
        #         params['end_time'] = params['current_run_time'] + attempt_run_time
        params['docking_time_s'] = todo
#--- TODO END DOCK

#--- BEGIN COMMON
#--- END COMMON
        """

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
            log.error('SUBMIT event encountered that is not a SUCCESS nor a FAIL status; skipping')

        logging.debug('Exiting ScoreboardStatus._computeSecureOrReturn')


    #---------------------------------------------------------------------------
    @staticmethod
    def _recomputeScore(algorithm,
                        team_name,
                        station_type,
                        max_submit_events,
                        calc_current_attempt_score,
                        now):
        logging.debug('Entered ScoreboardStatus._recomputeScore({})'.format(team_name))

        (team_events, start_challenge_events, score, start_time) = ScoreboardStatus._getEvents(team_name, station_type, now)

        params = {}
        params['score'] = score
        params['time_to_exit'] = False
        params['num_failed_attempts'] = 0;
        params['current_run_time'] = 0
        params['docking_time_s'] = 0
        i = 0

        while not params['time_to_exit']:
            attempt_num = i + 1
            logging.debug('Not yet time to exit; processing attempt {} of {} for team {}'.format(attempt_num, start_challenge_events.count(), team_name))

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
                logging.debug('Challenge complete; time to exit')
                params['time_to_exit'] = True
                params['end_time'] = now

        """
        TODO
        params['docking_time_s'] = _computeDockingTime(todo)
        """
        duration_s = (params['end_time'] - start_time).total_seconds() + params['docking_time_s']

        logging.debug('Exiting ScoreboardStatus._recomputeScore()')
        return (params['score'], duration_s)

    #---------------------------------------------------------------------------
    @staticmethod
    def _recomputeTeamScore(team_name):
        logging.debug('Entered ScoreboardStatus._recomputeTeamScore')

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
                "team_id"         : "TODO (team_id)",
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

        font_size = 24

        img = Image.new("RGBA", (img_width, img_height), (255, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        fonts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/scoreboard/fonts')
        font = ImageFont.truetype(os.path.join(fonts_path, 'EnchantedPrairieDog.TTF'), font_size)
        (text_width, text_height) = draw.textsize(text, font=font)

        x = (img_width - text_width) / 2
        y = 0

        draw.ellipse((0, 0, img_width-1, img_height-1), fill=color['polygon'])

        draw.text((x, y), text, font=font, fill=color['text'])

        result = HttpResponse(content_type="image/png", status=200)
        img.save(result, "PNG")

        logging.debug('Exiting TeamIcon.get')
        return result
