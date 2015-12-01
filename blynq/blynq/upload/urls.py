# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('blynq.upload.views',
    url(r'^list/$', 'list', name='list'),
)