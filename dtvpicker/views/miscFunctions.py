#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module holds some utility functions that are used in the DTV Picker feature."""

from events.models import Event


def PDFGenAllowed():
    """
    Checks if PDF Generation is allowed.
    Returns True if it is and False if not.
    PDF Generation is allowed if all events are locked.
    """

    eventList = Event.objects.all()

    for event in eventList:
        if event.lock_status != 'locked':
            return False
    return True


