"""ms.piservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    # Browser messages
    url(r'^$', views.index, name="index"),
    url(r'^index.html$', views.index, name="index"),
    
    # BRATA messages
    url(r'^register/(?P<team_passcode>[a-z]+[0-9]+)$', views.Register.as_view(), name="register"),
    url(r'^unregister/$', views.Unregister.as_view(), name="unregister"),
    url(r'^at_waypoint/(?P<lat>[0-9.-]+)/(?P<lon>[0-9.-]+)/$', views.AtWaypoint.as_view(), name="at_waypoint"),
    url(r'^start_challenge/(?P<station_id>[^/]+)/$', views.StartChallenge.as_view(), name="start_challenge"),
    url(r'^dock/(?P<station_id>[^/]+)/$', views.Dock.as_view(), name="dock"),

    # RPi station messages
    url(r'^join/$', views.Join.as_view(), name="join"),
    url(r'^heartbeat/$', views.Heartbeat.as_view(), name="heartbeat"),
    url(r'^leave/$', views.Leave.as_view(), name="leave"),
    url(r'^submit/$', views.Submit.as_view(), name="submit"),
    
    # Ajax requests
    url(r'^station_status/$', views.StationStatus.as_view(), name="station_status"),
    
    # Backward compatible 2015 message formats
    url(r'^brata-v00/register$', views.Register_2015.as_view(), name="register_2015"),
    url(r'^brata-v00/atWaypoint/(?P<waypointId>[^/#?]+)$', views.AtWaypoint_2015.as_view(), name="at_waypoint_2015"),
    url(r'^brata-v00/start_challenge/(?P<station_id>[^/#?]+)$', views.StartChallenge_2015.as_view(), name="start_challenge_2015"),
    url(r'^brata-v00/submit/(?P<station_id>[^/#?]+)$', views.Submit_2015.as_view(), name="submit_2015"), # this one needs a little work
]

# Test commands:
# (These commands use the "httpie" http utility)
#
# http POST :8000
# http --json POST :8000/piservice/register/ Content-type:application/json Accept:application/json team_id="Dev Team" brata_version="01"
# http --json POST :8000/piservice/join/ Content-type:application/json Accept:application/json host="First RPi Station" pi_type="B+" station_type=1
# http --json POST :8000/piservice/leave/ Content-type:application/json Accept:application/json station_id="8:8b14"
