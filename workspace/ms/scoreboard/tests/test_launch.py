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


class ScoreboardStatusLaunchTestCase(TestCase):
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
        actualScore = actual['launch_score']
        actualDuration_s = actual['launch_duration_s']

        self.assertEqual(expectedScore, actualScore)
        self.assertEqual(expectedDuration_s, actualDuration_s)

    def setUp(self):
        PiEvent._meta.get_field("time").auto_now_add = False

        self._serialNum = 1
        self._setUpStations()
        self._setUpTeams()
        self._setUpEvents()

    def test_recomputeLaunchScore_noEvents(self):
        PiEvent.objects.all().delete()
        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_noEventStartedEvent(self, side_effect=_mocked_utcNow):
        PiEvent.objects.all().delete()
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_eventsBeforeEventStartedEvent(self, side_effect=_mocked_utcNow):
        PiEvent.objects.all().delete()

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            pi = self.launchStation,
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
    def test_recomputeLaunchScore_noStartChallengeEvents(self, side_effect=_mocked_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2001, 1, 1, 0, 0, 0).replace(tzinfo=utc),
            type = PiEvent.REGISTER_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 0
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventSameTimestampNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2001, 1, 1, 0, 0, 0).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 1
        expectedDuration_s = 0
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampNoSuccessFail(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 1
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampOneSuccessNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 3
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampOneSuccessWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 3
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampOneFailNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        expectedScore = 2
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampOneFailWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 2
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampTwoSuccessNoConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 57, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 5
        expectedDuration_s = 130
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampTwoSuccessWithConclude(self, mock_utcNow):
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 57, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 5
        expectedDuration_s = 128
        self._verify(expectedScore, expectedDuration_s)


    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampOneSuccessOneFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        expectedScore = 4
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampOneSuccessOneFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 4
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampTwoFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        expectedScore = 3
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampTwoFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 3
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampThreeSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 7
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampThreeSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 7
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessSuccessFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        expectedScore = 6
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessSuccessFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 6
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 6
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 6
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        expectedScore = 5
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 5
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 6
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 6
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        expectedScore = 5
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 5
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailFailSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        expectedScore = 5
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailFailSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 5
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampThreeFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        expectedScore = 4
        expectedDuration_s = 10
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampThreeFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        expectedScore = 4
        expectedDuration_s = 8
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFourSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 9
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFourSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 9
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessSuccessSuccessFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 8
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessSuccessSuccessFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 8
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessSuccessFailSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 8
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessSuccessFailSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 8
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessSuccessFailFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessSuccessFailFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailSuccessSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 8
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailSuccessSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 8
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailSuccessFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailSuccessFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailFailSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailFailSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailFailFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 6
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampSuccessFailFailFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 6
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessSuccessSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 8
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessSuccessSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 8
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessSuccessFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessSuccessFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessFailSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessFailSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessFailFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 6
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailSuccessFailFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 6
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailFailSuccessSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailFailSuccessSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 7
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailFailSuccessFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 6
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailFailSuccessFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 6
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailFailFailSuccessNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 6
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFailFailFailSuccessWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.SUCCESS_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 6
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFourFailNoConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 5
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventEarlierTimestampFourFailWithConclude(self, mock_utcNow):
        
        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 50).replace(tzinfo=utc),
            type = PiEvent.START_CHALLENGE_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 54).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 55).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 56).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 57).replace(tzinfo=utc),
            type = PiEvent.SUBMIT_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation,
            status = PiEvent.FAIL_STATUS
        )

        e = PiEvent.objects.create(
            time = datetime(2000, 12, 31, 23, 59, 58).replace(tzinfo=utc),
            type = PiEvent.EVENT_CONCLUDED_MSG_TYPE,
            team = self.team1,
            pi = self.launchStation
        )

        # 4th success/fail stops the attempt; time does not continue ticking
        expectedScore = 5
        expectedDuration_s = 7
        self._verify(expectedScore, expectedDuration_s)

    @mock.patch('scoreboard.views._utcNow', side_effect=_mocked_utcNow)
    def test_recomputeLaunchScore_onlyOneStartChallengeEventLaterTimestamp(self, mock_utcNow):
        pass # Don't worry about later timestamps
