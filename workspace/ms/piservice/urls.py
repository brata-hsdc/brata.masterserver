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
    url(r'^register/$', views.Register.as_view(), name="register"),
#     url(r'^register/brata-(?P<brataVersion>[0-9]+)', views.Register.as_view(), name="register-brata"),

    # RPi station messages
    url(r'^join/$', views.Join.as_view(), name="join"),
    url(r'^leave/(?P<station_id>[0-9]+)', views.Leave.as_view(), name="leave"),
]

# Test commands:
# (These commands use the "httpie" http utility)
#
# http POST :8000
# http --json POST :8000/piservice/register/ Content-type:application/json Accept:application/json team_id="Dev Team" brata_version="01"
# http --json POST :8000/piservice/join/ Content-type:application/json Accept:application/json station_id="First RPi Station"
# http --json POST :8000/piservice/leave/12345 Content-type:application/json Accept:application/json
