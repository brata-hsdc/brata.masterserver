from django.test import TestCase
from django.utils.timezone import utc
from datetime import datetime
import logging
import mock
from dbkeeper.models import Organization, Team, Setting
from piservice.models import PiStation, PiEvent
import scoreboard.views as target

def _mocked_utcNow():
    return datetime(2001, 1, 1, 0, 0, 0).replace(tzinfo=utc)


class ScoreboardStatusSecureTestCase(TestCase):
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
        actualScore = actual['secure_score']
        actualDuration_s = actual['secure_duration_s']

        self.assertEqual(expectedScore, actualScore)
        self.assertEqual(expectedDuration_s, actualDuration_s)

    def setUp(self):
        PiEvent._meta.get_field("time").auto_now_add = False

        self._serialNum = 1
        self._setUpStations()
        self._setUpTeams()
        self._setUpEvents()

    def test_recomputeSecureScore_noEvents(self):
        PiEvent.objects.all().delete()
        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_noEventStartedEvent(self, side_effect=_mocked_utcNow):
        PiEvent.objects.all().delete()
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_eventsBeforeEventStartedEvent(self, side_effect=_mocked_utcNow):
        PiEvent.objects.all().delete()

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            pi = self.secureStation,
            team = self.team1,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 59).replace(tzinfo=utc),
            type = PiEvent.EVENT_STARTED_MSG_TYPE
        )

        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_noStartChallengeEvents(self, side_effect=_mocked_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2001, 1, 1, 0, 0, 0).replace(tzinfo=utc),
            type = PiEvent.REGISTER_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_onlyOneStartChallengeEventSameTimestampNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2001, 1, 1, 0, 0, 0).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 1
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_onlyOneStartChallengeEventEarlierTimestampNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 1
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_onlyOneStartChallengeEventEarlierTimestampSuccessNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 9
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_onlyOneStartChallengeEventEarlierTimestampSuccessWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 9
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_onlyOneStartChallengeEventEarlierTimestampFailNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        expectedScore = 5
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_onlyOneStartChallengeEventEarlierTimestampFailWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 5
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_twoStartChallengeEventsEarlierTimestampFailNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 5
        expectedDuration_s = 14
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_twoStartChallengeEventsEarlierTimestampFailSuccessNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 9
        expectedDuration_s = 6
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_twoStartChallengeEventsEarlierTimestampFailSuccessWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 9
        expectedDuration_s = 6
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_twoStartChallengeEventsEarlierTimestampFailFailNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 5
        expectedDuration_s = 14
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_twoStartChallengeEventsEarlierTimestampFailFailWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 5
        expectedDuration_s = 12
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_threeStartChallengeEventsEarlierTimestampFailFailNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 5
        expectedDuration_s = 14
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_threeStartChallengeEventsEarlierTimestampFailFailSuccessNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 9
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_threeStartChallengeEventsEarlierTimestampFailFailSuccessWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 9
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_threeStartChallengeEventsEarlierTimestampFailFailFailNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        expectedScore = 5
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_threeStartChallengeEventsEarlierTimestampFailFailFailWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 46).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 48).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 52).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.secureStation
        )

        expectedScore = 5
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeSecureScore_onlyOneStartChallengeEventLaterTimestamp(self, mock_utcNow):
        pass # Don't worry about later timestamps
