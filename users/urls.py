# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import SignupView


urlpatterns = patterns('',
    url('^signup$', SignupView.as_view(), name='signup'),
)
