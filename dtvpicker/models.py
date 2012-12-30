#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.sitemaps import ping_google

from events.models import Event

from dtvpicker.VenueChoices import BLOCK_CHOICES

class Venue(models.Model):
    """
    The venue model is responsible for storing all the venues where events can be held.
    Venues are grouped under blocks.
    Ex: CRC 101-103, 201-205, 301-305 come under the CRC block.
    """
    title = models.CharField(max_length = 32, verbose_name = 'Venue Name')
    block = models.CharField(max_length = 8, choices = BLOCK_CHOICES)
    
    def __unicode__(self):
        return '%s' % (self.title,)
        
class VenueGroupAlias(models.Model):
    """
    This model holds various groups of venues and their combined alias.
    E.g., CRC 101-103 is 'CRC Ground Floor', CRC 101-305 is 'CRC', etc.
    """
    venues = models.ManyToManyField(Venue, help_text = 'Select all the venues that you want to give an alias for.', null = False, blank = False)
    alias = models.CharField(max_length = 32, help_text = 'Key in an alias for the selected venues.')
    
    def __unicode__(self):
        return '%s' % (self.alias,)
        
    def display_venues(self):
        """
        This function creates a neat string representation for the Many to Many field venues.
        The individual venues must be separated by commas and the block name should be displayed once at the start.
        Also, if the venue name has the block name already in it, it should be removed.
        """
        disp_string = ''
        
        # Get the venues to be displayed.
        venueList = self.venues.all()
        
        # Separate all the venues with commas. 
        # Also check if each individual venue name already has the block name. If so, remove it.
        for venue in venueList:
            if venue.title[:len(venue.block)] == venue.block:
                extraChars = 0
                while ((len(venue.block) + extraChars < len(venue.title))) and (venue.title[len(venue.block)+extraChars] == ' '):
                    extraChars += 1
                disp_string += venue.title[len(venue.block)+extraChars:] + ', '
            else:
                disp_string += venue.title + ', '
            
        disp_string = disp_string[:-2]  # Remove the last two characters (which are an extra comma and space added after each venue)
        
        disp_string = venueList[0].block + ' ' + disp_string  # Prepend the block name to the venue list

        return disp_string

class SubEvent(models.Model):

    """
    A sub-event is, e.g. Prelims 1, Finals, Workshop 2, Lecture 3, etc., of an event.
    """
    title = models.CharField(max_length = 32, 
                             help_text = 'Title of the sub-event. E.g. "Prelims 1", "Finals", "Lecture 2", "Workshop 3", etc.', 
                             verbose_name = "Sub-Event Title")
    start_date_and_time = models.DateTimeField(blank = True, null = True, help_text = 'When will this sub-event start? (yyyy-mm-dd hh:mm:ss)')
    end_date_and_time = models.DateTimeField(blank = True, null = True, help_text = 'When will this sub-event end? (yyyy-mm-dd hh:mm:ss)')
    venue = models.ManyToManyField(Venue, blank = True, null = True, help_text = 'Where will this sub-event be held?')
    event = models.ForeignKey(Event)
    last_modified = models.DateTimeField(editable = False, auto_now = True)

    def __unicode__(self):
        return '%s' % (self.title,)
        
    def display_venue(self):
        """
        This function creates a neat string representation for the Many to Many field venue.
        If the venues stored in venue match the venues stored under any alias, the alias will be displayed.
        Else, the individual venues must be separated by commas and the block name should be displayed once at the start.
        """
        disp_string = ''
        
        # Get the venues to be displayed.
        venueList = self.venue.all()
        
        # Get a list of all the VenueGroupAlias objects stored in the db.
        venueAliases = VenueGroupAlias.objects.all()
        
        # Compare the venue sets of the each of the VenueGroupAlias objects with the venues to be displayed.
        for venueAlias in venueAliases:
            if set(venueAlias.venues.all()) == set(venueList):  # If any of them matches, it should be displayed instead of the individual venues.
                return venueAlias.alias
                
        # If none of the alias venue sets match, the individual venues should be separated by commas.
        # Also check if each individual venue name already has the block name. If so, remove it.
        for venue in venueList:
            if venue.title[:len(venue.block)] == venue.block:
                extraChars = 0
                while ((len(venue.block) + extraChars < len(venue.title))) and (venue.title[len(venue.block)+extraChars] == ' '):
                    extraChars += 1
                disp_string += venue.title[len(venue.block)+extraChars:] + ', '
            else:
                disp_string += venue.title + ', '
            
        if disp_string != '':
            disp_string = disp_string[:-2]  # Remove the last two characters (which are an extra comma and space added after each venue)
            disp_string = venueList[0].block + ' ' + disp_string  # Prepend the block name to the venue list

        return disp_string

    def save(self, force_insert=False, force_update=False):
	super(SubEvent, self).save(force_insert, force_update)
	try:
		ping_google()
	except Exception:
		pass

