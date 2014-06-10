# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Guest(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u'Name'))
    position = models.CharField(max_length=63, verbose_name=_(u'Position'))
    department = models.CharField(max_length=255,
                                  verbose_name=_(u'Department'))
    email = models.EmailField()
