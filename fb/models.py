#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from events.models import Event


# Create your models here.

class sampark(models.Model):
  place = models.CharField(max_length = 20)
  headerlink = models.CharField(max_length = 100)
  writeup = models.CharField(max_length=500)
  albumid = models.BigIntegerField()

  def __unicode__(self):
    return '%s' % self.place


