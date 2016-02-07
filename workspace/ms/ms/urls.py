"""ms URL Configuration

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

from piservice import urls as piservice_urls
from dbkeeper import urls as dbkeeper_urls
from scoreboard import urls as scoreboard_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^piservice/', include(piservice_urls)),
    url(r'^serve_pi/', include(piservice_urls)),  # appetizing alias for piservice
    url(r'^m/', include(piservice_urls)),  # alias for 2015 backward compatibility
    url(r'^dbkeeper/', include(dbkeeper_urls)),
    url(r'^hsdc/', include(dbkeeper_urls)), # alias for dbkeeper for student test pages
    url(r'^scoreboard/', include(scoreboard_urls)),
]
