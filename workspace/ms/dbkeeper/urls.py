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
    url(r'^test.html$', views.test, name="test"),
    url(r'^remotetest/$', views.regtest.as_view(), name="regtest"),
    url(r'^regtest_team/(?P<pass_code>[^/]+)/$', views.regtest_team.as_view(), name="regtest_team"),
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
    ]

# Test commands:
#
# http://localhost:8000/
# http://localhost:8000/index.html
# http://localhost:8000/add         (404)
# http://localhost:8000/add/org
# http://localhost:8000/add/organization
# http://localhost:8000/add/user
