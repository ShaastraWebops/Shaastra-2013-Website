#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO(Anant, anant.girdhar@gmail.com): We need a venue choice list in place of the temporary one used here.

"""
This file holds a list of all venues where events can be held.
The choices are in the format: (venue_code, venue_name).
This file may be removed if it is not required.
The venues have now been moved to a model.
"""

VENUE_CHOICES = (
    (u'CRC', u'Class Room Complex'),
    (u'CLT', u'Cebtral Lecture Theatre'),
    (u'SAC', u'Students Activity Centre'),
    (u'LIB', u'Central Library'),
    (u'OAT', u'Open Air Theatre'),
    (u'PhLT', u'Physics Lecture Theatre'),
    (u'ChLT', u'Chemistry Lecture Theatre'),
    (u'PHY', u'Physics Deptartment'),
    (u'CHEM', u'Chemistry Deptartment'),
    (u'BT', u'Biotech Deptartment'),
    )

BLOCK_CHOICES = ((u'BSB',  u'Building Sciences Block'),
                 (u'BT',   u'BT Department'),
                 (u'CH',   u'Chemistry Department'),
                 (u'CLT',  u'Central Lecture Theatre Area'),
                 (u'CRC',  u'Class Room Complex'),
                 (u'CS',   u'CS Department'),
                 (u'DoMS', u'Department of Management Studies'),
                 (u'ED',   u'Engineering Design Department'),
                 (u'Elec', u'Electrical Department'),
                 (u'HSB',  u'Humanities and Sciences Block'),
                 (u'ICSR', u'IC & SR'),
                 (u'KV',   u'KV Grounds'),
                 (u'Lib',  u'Central Library'),
                 (u'MSB',  u'Mechanical Sciences Block'),
                 (u'OAT',  u'Open Air Theatre'),
                 (u'RP',   u'Research Park'),
                 (u'SAC',  u'Student\'s Activity Center'),
                 (u'STAD', u'Stadium'),
                 (u'WS',   u'Central Workshop'),
                 (u'Misc', u'Miscellaneous Venues'),
                )
