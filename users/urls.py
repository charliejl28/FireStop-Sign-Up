# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import SignupView, POSTPilot


urlpatterns = patterns('',
    url('^signup$', SignupView.as_view(), name='signup'),
    url('^signup/pilot$', POSTPilot.as_view(), name='post_pilot'),
)
