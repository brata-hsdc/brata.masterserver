"""ms.dbkeeper URL Configuration

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
    url(r'^$', views.index, name="index"),
    url(r'^index.html$', views.index, name="index"),
    url(r'^remotetest/$', views.regtest.as_view(), name="regtest"), # thisis the student main test page already advertised
    url(r'^test/$', views.regtest.as_view(), name="regtest"), # this is the student test main page (we should remove or rename test.html)
    url(r'^regtest_team/(?P<pass_code>[^/]+)/$', views.regtest_team.as_view(), name="regtest_team"),
    url(r'^navtest_team/(?P<pass_code>[^/]+)/(?P<lat1>[0-9.-]+)/(?P<lon1>[0-9.-]+)/(?P<lat2>[0-9.-]+)/(?P<lon2>[0-9.-]+)/(?P<lat3>[0-9.-]+)/(?P<lon3>[0-9.-]+)/(?P<lat4>[0-9.-]+)/(?P<lon4>[0-9.-]+)/(?P<school_name>[^/]*)/$', views.NavTestTeam.as_view(), name="navtest_team"),
    url(r'^station_status/$', views.station_status, name="station_status_page"),
    url(r'^add/org/$', views.AddOrganization.as_view(), name="AddOrg"),
    url(r'^add/organization/$', views.AddOrganization.as_view(), name="AddOrganization"),
    url(r'^add/user/$', views.AddUser.as_view(), name="AddUser"),
    url(r'^add/team/$', views.AddTeam.as_view(), name="AddTeam"),
    url(r'^add/launchparams/$', views.AddLaunchParams.as_view(), name="AddLaunchParams"),
    url(r'^add/dockparams/$', views.AddDockParams.as_view(), name="AddDockParams"),
    url(r'^add/secureparams/$', views.AddSecureParams.as_view(), name="AddSecureParams"),
    url(r'^add/returnparams/$', views.AddReturnParams.as_view(), name="AddReturnParams"),
    url(r'^checkin/team/$', views.CheckInTeam.as_view(), name="CheckInTeam"),
    url(r'^save/settings/$', views.SaveSettings, name="SaveSettings"),
    url(r'^save/settings/confirmed/$', views.SaveSettingsConfirmed, name="SaveSettingsConfirmed"),  # save Setting table to CSV file
    url(r'^load/settings/$', views.LoadSettings.as_view(), name="LoadSettings"),  # load Setting table from CSV file
    url(r'^competition/start/$', views.CompetitionStart.as_view(), name="CompetitionStart"),  # clear the PiEvent table and/or insert a Competition Start event 
    url(r'^competition/end/$', views.CompetitionEnd.as_view(), name="CompetitionEnd"),  # insert a Competition End event 
    url(r'^add/logmsg/$', views.LogMessage.as_view(), name="LogMessage"),  # insert a LOG_MESSAGE_MSG_TYPE event to mark something
    ]

# Test commands:
#
# http://localhost:8000/
# http://localhost:8000/index.html
# http://localhost:8000/add         (404)
# http://localhost:8000/add/org
# http://localhost:8000/add/organization
# http://localhost:8000/add/user
