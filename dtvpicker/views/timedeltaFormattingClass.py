#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module holds the necessary modules for formatting timedelta objects."""

from string import Template


# Code copied from http://stackoverflow.com/questions/8906926/formatting-python-timedelta-objects and then modified.

class DeltaTemplate(Template):

    delimiter = '%'


def strfdelta(tdelta, fmt):
    d = {'D': tdelta.days}
    (d['H'], rem) = divmod(tdelta.seconds, 3600)
    (d['M'], d['S']) = divmod(rem, 60)
    d['H'] += d['D'] * 24
    del d['D']
    if d['H'] < 10:
        d['H'] = '0' + str(d['H'])
    else:
        d['H'] = str(d['H'])

    if d['M'] < 10:
        d['M'] = '0' + str(d['M'])
    else:
        d['M'] = str(d['M'])

    if d['S'] < 10:
        d['S'] = '0' + str(d['S'])
    else:
        d['S'] = str(d['S'])

    t = DeltaTemplate(fmt)
    return t.substitute(**d)


