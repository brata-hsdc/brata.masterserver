"""ms.scoreboard URL Configuration

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

    # Ajax requests
    url(r'^scoreboard_status/$', views.ScoreboardStatus.as_view(), name="scoreboard_status"),
    url(r'^team_icon/(?P<team_name>.+)/$', views.TeamIcon.as_view(), name="team_icon"),
]

# Test commands:
#
# http://localhost:8000/
# http://localhost:8000/index.html
# http://localhost:8000/scoreboard
# http://localhost:8000/scoreboard/scoreboard_status/
# http://localhost:8000/scoreboard/images/...
