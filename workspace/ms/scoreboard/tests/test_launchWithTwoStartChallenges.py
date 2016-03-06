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


#class ScoreboardStatusLaunchTestCase(TestCase):
    # Don't bother with this. For Launch, the teams will only get one pass
    # through the course; they will get multiple attempts during the pass.
    # Therefore, there is no second nor third START_CHALLENGE.