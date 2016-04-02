from django.test import TestCase
from django.utils.timezone import utc
from datetime import datetime
import json
import logging
import mock
from dbkeeper.models import Organization, Team, Setting
from piservice.models import PiStation, PiEvent
import scoreboard.views as target

def _mocked_utcNow():
    return datetime(2001, 1, 1, 0, 0, 0).replace(tzinfo=utc)


class ScoreboardStatusDockTestCase(TestCase):
    def _setUpStations(self):
        self.launchStation = PiStation.objects.create(
            station_type = PiStation.LAUNCH_STATION_TYPE,
            serial_num = self._serialNum
        )

        self._serialNum += 1

        self.dockStation = PiStation.objects.create(
            station_type = PiStation.DOCK_STATION_TYPE,
            serial_num = self._serialNum
        )

        self._serialNum += 1

        self.secureStation = PiStation.objects.create(
            station_type = PiStation.SECURE_STATION_TYPE,
            serial_num = self._serialNum
        )

        self._serialNum += 1

        self.returnStation = PiStation.objects.create(
            station_type = PiStation.RETURN_STATION_TYPE,
            serial_num = self._serialNum
        )

        self._serialNum += 1

        self.station = self.dockStation

    def _setUpTeams(self):
        org = Organization.objects.create(
            name = "School 1",
            type = Organization.SCHOOL_TYPE
        )

        self.team1Name = "Team 1"

        self.team1 = Team.objects.create(
            name = self.team1Name,
            organization = org
        )

    def _setUpEvents(self):
        # Some tests don't need these events. If not needed for a particular
        # test, use PiEvent.objects.all().delete()
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 0, 0).replace(tzinfo=utc),
            type = PiEvent.EVENT_STARTED_MSG_TYPE
        )

    def _verify(self,
                expectedScore,
                expectedDuration_s):
        actual = target._recomputeTeamScore(self.team1Name)
        actualScore = actual['dock_score']
        actualDuration_s = actual['dock_duration_s']

        self.assertEqual(expectedScore, actualScore)
        self.assertEqual(expectedDuration_s, actualDuration_s)

    def setUp(self):
        PiEvent._meta.get_field("time").auto_now_add = False

        self._serialNum = 1
        self._setUpStations()
        self._setUpTeams()
        self._setUpEvents()

        self._watchingTime_s = 45

        Setting.objects.create(name = 'DNF_TIME_PENALTY_FACTOR', value = str(-2000))
        Setting.objects.create(name = 'DOCK_SIM_PLAYBACK_TIME_S', value = str(self._watchingTime_s))

    def test_recomputeDockScore_noEvents(self):
        PiEvent.objects.all().delete()
        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_noEventStartedEvent(self, side_effect=_mocked_utcNow):
        PiEvent.objects.all().delete()
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": 0, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_eventsBeforeEventStartedEvent(self, side_effect=_mocked_utcNow):
        PiEvent.objects.all().delete()

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            pi = self.station,
            team = self.team1,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": 0, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 59).replace(tzinfo=utc),
            type = PiEvent.EVENT_STARTED_MSG_TYPE
        )

        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_noStartChallengeEvents(self, side_effect=_mocked_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2001, 1, 1, 0, 0, 0).replace(tzinfo=utc),
            type = PiEvent.REGISTER_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_onlyOneStartChallengeEventSameTimestampNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2001, 1, 1, 0, 0, 0).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 1
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_onlyOneStartChallengeEventEarlierTimestampNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 1
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_onlyOneStartChallengeEventEarlierTimestampSuccessNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime_s = 10
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        expectedScore = 9
        expectedDuration_s = 6 - self._watchingTime_s + actualTime_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_onlyOneStartChallengeEventEarlierTimestampSuccessWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime_s = 68
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 9
        expectedDuration_s = 6 - self._watchingTime_s + actualTime_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_onlyOneStartChallengeEventEarlierTimestampFailOutcomeDnf2xPenaltyNoConclude(self, mock_utcNow):
        dnfPenalty = 2

        Setting.objects.all().delete()
        Setting.objects.create(name = 'DNF_TIME_PENALTY_FACTOR', value = str(-1000 * dnfPenalty))

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime_s = 213
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime_s, "fail_message": "OUTCOME_DNF"}, separators=(',',':'))
        )

        expectedScore = 1
        expectedDuration_s = 10 - self._watchingTime_s + (actualTime_s * dnfPenalty)
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_onlyOneStartChallengeEventEarlierTimestampFailOutcomeDnf3xPenaltyNoConclude(self, mock_utcNow):
        dnfPenalty = 3

        Setting.objects.all().delete()
        Setting.objects.create(name = 'DNF_TIME_PENALTY_FACTOR', value = str(-1000 * dnfPenalty))

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime_s = 47
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime_s, "fail_message": "OUTCOME_DNF"}, separators=(',',':'))
        )

        expectedScore = 1
        expectedDuration_s = 10 - self._watchingTime_s + (actualTime_s * dnfPenalty)
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_onlyOneStartChallengeEventEarlierTimestampFailOutcomeDnf8xPenaltyNoConclude(self, mock_utcNow):
        dnfPenalty = 8

        Setting.objects.all().delete()
        Setting.objects.create(name = 'DNF_TIME_PENALTY_FACTOR', value = str(-1000 * dnfPenalty))

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime_s = 33
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime_s, "fail_message": "OUTCOME_DNF"}, separators=(',',':'))
        )

        expectedScore = 1
        expectedDuration_s = 10 - self._watchingTime_s + (actualTime_s * dnfPenalty)
        self._verify(expectedScore, expectedDuration_s)


    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_onlyOneStartChallengeEventEarlierTimestampFailNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime_s = 1684
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        expectedScore = 1
        expectedDuration_s = 10 - self._watchingTime_s + actualTime_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_onlyOneStartChallengeEventEarlierTimestampFailWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime_s = 2000
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 1
        expectedDuration_s = 8 - self._watchingTime_s + actualTime_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_twoStartChallengeEventsEarlierTimestampSuccessNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime_s = 3000
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 9
        expectedDuration_s = 6 - self._watchingTime_s + actualTime_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_twoStartChallengeEventsEarlierTimestampSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 319
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 4897
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        expectedScore = 9
        expectedDuration_s = 6 - self._watchingTime_s + actualTime1_s # ignore actualTime2_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_twoStartChallengeEventsEarlierTimestampSuccessSuccess(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 3213
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 228
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        expectedScore = 9
        expectedDuration_s = 6 - self._watchingTime_s + actualTime1_s # ignore acutalTime2_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_twoStartChallengeEventsEarlierTimestampFailNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime_s = 283
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 1
        expectedDuration_s = 14 - self._watchingTime_s + actualTime_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_twoStartChallengeEventsEarlierTimestampFailSuccessNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 9385
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 332
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        expectedScore = 9
        expectedDuration_s = 6 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_twoStartChallengeEventsEarlierTimestampFailSuccessWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 123
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 456
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 9
        expectedDuration_s = 6 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_twoStartChallengeEventsEarlierTimestampFailFailNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 345
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 678
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 1
        expectedDuration_s = 14 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_twoStartChallengeEventsEarlierTimestampFailFailWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 4567
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 678
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 1
        expectedDuration_s = 12 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_threeStartChallengeEventsEarlierTimestampFailFailNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 567
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 890
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 1
        expectedDuration_s = 14 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_threeStartChallengeEventsEarlierTimestampFailFailSuccessNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 678
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 789
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime3_s = 7654
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime3_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        expectedScore = 9
        expectedDuration_s = 10 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s - self._watchingTime_s + actualTime3_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_threeStartChallengeEventsEarlierTimestampFailFailSuccessWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 321
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 654
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime3_s = 987
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime3_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 9
        expectedDuration_s = 10 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s - self._watchingTime_s + actualTime3_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_threeStartChallengeEventsEarlierTimestampFailFailFailNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 32
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 54
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime3_s = 76
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime3_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        expectedScore = 5
        expectedDuration_s = 10 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s - self._watchingTime_s + actualTime3_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_threeStartChallengeEventsEarlierTimestampFailFailFailWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 23
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 45
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime3_s = 67
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime3_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 5
        expectedDuration_s = 10 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s - self._watchingTime_s + actualTime3_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_fourStartChallengeEventsEarlierTimestampFailFailFailNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 123
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 45
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime3_s = 6789
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime3_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        expectedScore = 5
        expectedDuration_s = 10 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s - self._watchingTime_s + actualTime3_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_fourStartChallengeEventsEarlierTimestampFailFailFailFailNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 122
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 233
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime3_s = 344
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime3_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime4_s = 455
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime4_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        expectedScore = 5
        expectedDuration_s = 10 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s - self._watchingTime_s + actualTime3_s # ignore actualTime4_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_fourStartChallengeEventsEarlierTimestampFailFailFailSuccessNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime1_s = 1223
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime1_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime2_s = 2334
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime2_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime3_s = 3445
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.FAIL_STATUS,
            data = json.dumps({"candidate_answer": actualTime3_s, "fail_message": "OUTCOME_TOO_SLOW"}, separators=(',',':'))
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.station
        )

        actualTime4_s = 4556
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.station,
            status = PiEvent.SUCCESS_STATUS,
            data = json.dumps({"candidate_answer": actualTime4_s, "fail_message": "OUTCOME_SUCCESS"}, separators=(',',':'))
        )

        expectedScore = 5
        expectedDuration_s = 10 - self._watchingTime_s + actualTime1_s - self._watchingTime_s + actualTime2_s - self._watchingTime_s + actualTime3_s # ignore actualTime4_s
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeDockScore_onlyOneStartChallengeEventLaterTimestamp(self, mock_utcNow):
        pass # Don't worry about later timestamps

# TODO
"""
[Wed Mar 30 11:47:11.797470 2016] [wsgi:error] [pid 649:tid 1938814000] Internal Server Error: /scoreboard/scoreboard_status/
[Wed Mar 30 11:47:11.798282 2016] [wsgi:error] [pid 649:tid 1938814000] Traceback (most recent call last):
[Wed Mar 30 11:47:11.798657 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/usr/local/lib/python2.7/dist-packages/django/core/handlers/base.py", line 149, in get_response
[Wed Mar 30 11:47:11.798973 2016] [wsgi:error] [pid 649:tid 1938814000]     response = self.process_exception_by_middleware(e, request)
[Wed Mar 30 11:47:11.799340 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/usr/local/lib/python2.7/dist-packages/django/core/handlers/base.py", line 147, in get_response
[Wed Mar 30 11:47:11.799633 2016] [wsgi:error] [pid 649:tid 1938814000]     response = wrapped_callback(request, *callback_args, **callback_kwargs)
[Wed Mar 30 11:47:11.799906 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/usr/local/lib/python2.7/dist-packages/django/views/generic/base.py", line 68, in view
[Wed Mar 30 11:47:11.800181 2016] [wsgi:error] [pid 649:tid 1938814000]     return self.dispatch(request, *args, **kwargs)
[Wed Mar 30 11:47:11.800442 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/usr/local/lib/python2.7/dist-packages/django/views/generic/base.py", line 88, in dispatch
[Wed Mar 30 11:47:11.800711 2016] [wsgi:error] [pid 649:tid 1938814000]     return handler(request, *args, **kwargs)
[Wed Mar 30 11:47:11.800920 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/views.py", line 507, in get
[Wed Mar 30 11:47:11.801131 2016] [wsgi:error] [pid 649:tid 1938814000]     s = _recomputeTeamScore(t.name)
[Wed Mar 30 11:47:11.801335 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/views.py", line 392, in _recomputeTeamScore
[Wed Mar 30 11:47:11.801824 2016] [wsgi:error] [pid 649:tid 1938814000]     now)
[Wed Mar 30 11:47:11.802105 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/views.py", line 358, in _recomputeScore
[Wed Mar 30 11:47:11.802380 2016] [wsgi:error] [pid 649:tid 1938814000]     now)
[Wed Mar 30 11:47:11.802584 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/views.py", line 50, in _computeDock
[Wed Mar 30 11:47:11.802799 2016] [wsgi:error] [pid 649:tid 1938814000]     submit_message = params['submit_events'][attempt_num - 1]
[Wed Mar 30 11:47:11.803218 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/usr/local/lib/python2.7/dist-packages/django/db/models/query.py", line 297, in __getitem__
[Wed Mar 30 11:47:11.803496 2016] [wsgi:error] [pid 649:tid 1938814000]     return list(qs)[0]
[Wed Mar 30 11:47:11.803760 2016] [wsgi:error] [pid 649:tid 1938814000] IndexError: list index out of range
[Wed Mar 30 11:47:11.805178 2016] [wsgi:error] [pid 649:tid 1938814000] ERROR    Internal Server Error: /scoreboard/scoreboard_status/
[Wed Mar 30 11:47:11.805639 2016] [wsgi:error] [pid 649:tid 1938814000] Traceback (most recent call last):
[Wed Mar 30 11:47:11.805950 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/usr/local/lib/python2.7/dist-packages/django/core/handlers/base.py", line 149, in get_response
[Wed Mar 30 11:47:11.806265 2016] [wsgi:error] [pid 649:tid 1938814000]     response = self.process_exception_by_middleware(e, request)
[Wed Mar 30 11:47:11.806535 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/usr/local/lib/python2.7/dist-packages/django/core/handlers/base.py", line 147, in get_response
[Wed Mar 30 11:47:11.806806 2016] [wsgi:error] [pid 649:tid 1938814000]     response = wrapped_callback(request, *callback_args, **callback_kwargs)
[Wed Mar 30 11:47:11.807152 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/usr/local/lib/python2.7/dist-packages/django/views/generic/base.py", line 68, in view
[Wed Mar 30 11:47:11.807453 2016] [wsgi:error] [pid 649:tid 1938814000]     return self.dispatch(request, *args, **kwargs)
[Wed Mar 30 11:47:11.807669 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/usr/local/lib/python2.7/dist-packages/django/views/generic/base.py", line 88, in dispatch
[Wed Mar 30 11:47:11.807880 2016] [wsgi:error] [pid 649:tid 1938814000]     return handler(request, *args, **kwargs)
[Wed Mar 30 11:47:11.808283 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/views.py", line 507, in get
[Wed Mar 30 11:47:11.808565 2016] [wsgi:error] [pid 649:tid 1938814000]     s = _recomputeTeamScore(t.name)
[Wed Mar 30 11:47:11.808772 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/views.py", line 392, in _recomputeTeamScore
[Wed Mar 30 11:47:11.809294 2016] [wsgi:error] [pid 649:tid 1938814000]     now)
[Wed Mar 30 11:47:11.809565 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/views.py", line 358, in _recomputeScore
[Wed Mar 30 11:47:11.809837 2016] [wsgi:error] [pid 649:tid 1938814000]     now)
[Wed Mar 30 11:47:11.810093 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/opt/designchallenge2016/brata.masterserver/workspace/ms/scoreboard/views.py", line 50, in _computeDock
[Wed Mar 30 11:47:11.810360 2016] [wsgi:error] [pid 649:tid 1938814000]     submit_message = params['submit_events'][attempt_num - 1]
[Wed Mar 30 11:47:11.810618 2016] [wsgi:error] [pid 649:tid 1938814000]   File "/usr/local/lib/python2.7/dist-packages/django/db/models/query.py", line 297, in __getitem__
[Wed Mar 30 11:47:11.810881 2016] [wsgi:error] [pid 649:tid 1938814000]     return list(qs)[0]
[Wed Mar 30 11:47:11.811086 2016] [wsgi:error] [pid 649:tid 1938814000] IndexError: list index out of range
"""


# TODO Jaron sent three failures, score was 1 instead of 5 after 3rd failure.

# TOOD Jaron finished all three attempts but clock still kept going



# Scoreboard
# 1. absent/present Registered indicator
# 2. make title larger and change to "Leaderboard"
# 3. fill width 100%
# 4. make 30 teams fit on the same page with roughly 20-30 chars
# 5. header row multiple lines--all text doesn't show up
# 6. don't need to show page footer; find another place for the attribution
# 7. put "Harris Design Challenge 2016" along the left-hand side
# 8. ranking
# 11. remove team logo if not implementing this time

# TODO Page has two jquery <script> tags--one looks WRONG_ARGUMENTS


# Enhancements
# 9. Change color (darker) for the ones that are zero (not started)
# 10. Set color brighter to stand out for the ones that are done
