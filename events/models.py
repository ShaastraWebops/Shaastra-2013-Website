#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#from users.models import Team
from django import forms
from django.forms import ModelForm
from chosen import forms as chosenforms
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.cache import cache
import os

EVENT_CATEGORIES = (
    ('Aerofest', 'Aerofest'),
    ('Coding', 'Coding'),
    ('Design and Build', 'Design and Build'),
    ('Involve', 'Involve'),
    ('Quizzes', 'Quizzes'),
    ('Online', 'Online'),
    ('Department Flagship', 'Department Flagship'),
    ('Spotlight', 'Spotlight'),
    ('Workshops', 'Workshops'),
    ('Exhibitions', 'Exhibitions and Shows'),
    ('Associated Events', 'Associated Events'),    
    ('Sampark', 'Sampark'),
    )

CATEGORY = (('Update', 'Update'), ('Announcement', 'Announcement'))


# Create your models here.

def upload_handler(model_name):

    def upload_func(instance, filename):
        return os.path.join(model_name, instance.title, filename)

    return upload_func


class Tag(models.Model):

    name = models.CharField(max_length=25)

    def __unicode__(self, *args, **kwargs):
        return self.name


class Event(models.Model):

    title = models.CharField(max_length=300)
    events_logo = models.FileField(upload_to=upload_handler('Events'),
                                   blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    category = models.CharField(max_length=50, choices=EVENT_CATEGORIES)
    lock_status = models.CharField(default='cannot_be_locked',
                                   max_length=20)
    unlock_reason = models.TextField(default='', blank=True)

    registrable_online = models.BooleanField(default=False,
            help_text='Can participants register online?')
    team_event = models.BooleanField(default=False,
            help_text='Is this a team event?')
    team_size_min = models.IntegerField(default=1,
            verbose_name='Minimum team size')
    team_size_max = models.IntegerField(default=1,
            verbose_name='Maximum team size')
            
    begin_registration = models.BooleanField(default=False,
            help_text='Mark as True to begin online registration')
    has_tdp = models.BooleanField(default=False,
            help_text='Does this event require participants to submit a TDP?'
            )
    has_questionnaire = models.BooleanField(default=False,
            help_text='Will the participant have to answer a questionnaire?'
            )
    fb_event_id = models.CharField(max_length=20, null=True)
    updated = models.BooleanField(default=False)
    sponsor_logo_url= models.CharField(max_length=150)
    sponsor_logo = models.FileField(upload_to=upload_handler('Events/Sponsors'),
                                   blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.title
        
    def clean(self):
        """
        This method will work to clean the instance of Event created.
        Custom validations to be performed:
            * If the event is not a team event, then the team sizes must not be specified.
            * If team sizes are not specified, they should be set to one each (individual participation).
            * Minimum team size should not be greater than the maximum team size.
        """
        # References:
        # https://docs.djangoproject.com/en/dev/ref/models/instances/#validating-objects
        # https://docs.djangoproject.com/en/dev/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
        # http://stackoverflow.com/questions/2117048/django-overriding-the-clean-method-in-forms-question-about-raising-errors

        errors = []
        super(Event, self).clean()  # Calling clean method of the super class
        try:
            team_event
            if team_size_min > team_size_max:
                errors.append(u'The minimum team size cannot be more than the maximum team size.')
            if team_size_max == 1:
                errors.append(u'The maximum team size is 1. Did you mean to make this a non-team event?')
        except:
            team_size_min = team_size_max = 1
        if not team_size_min:
            team_size_min = 1
        if not team_size_max:
            team_size_max = 1
        if errors:
            raise ValidationError(errors)

    def construct_dir_path(self):
        try:
            return settings.EVENT_DIR + 'event_' + str(self.id) + '/'
        except AttributeError:
            return 'events/event_' + str(self.id) + '/'

class EventSingularRegistration(models.Model):
    
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    
    def __unicode__(self):
        return '%s <- User: %s' % (event, user)
        
'''
class EventTeamRegistration(models.Model):
    
    team = models.ForeignKey(Team)
    event = models.ForeignKey(Event)
    
    def __unicode__(self):
        return '%s <- Team: %s' % (event, team)
'''

class Update(models.Model):

    subject = models.CharField(max_length=25)
    description = models.TextField()
    date = models.DateField(default=datetime.now)
    category = models.CharField(max_length=15, choices=CATEGORY,
                                help_text='You can add 4 updates and 1 announcement. Mark as announcement only if the information is of highest importance'
                                )
    event = models.ForeignKey(Event, null=True, blank=True)
    expired = models.BooleanField(default=False,
                                  help_text='Mark an update/announcement as expired if it is no longer relevant or you have more than 4 updates (or 1 announcement) '
                                  )


    def save(self, force_insert=False, force_update=False):
	super(Event, self).save(force_insert, force_update)
	try:
		ping_google()
	except Exception:
		pass

class Tab(models.Model):

    event = models.ForeignKey(Event, blank=True, null=True)
    title = models.CharField(max_length=30)
    text = models.TextField()
    pref = models.IntegerField(max_length=2, default=0, blank=False,
                               help_text='This is the order in which your tabs will be displayed on main site.'
                               )

#    def save(self):
#        cache.set(str(self.id)+"_event", str(self.event), 2592000)
#        cache.set(str(self.id)+"_title", str(self.title), 2592000)
#        cache.set(str(self.id)+"_text", str(self.text), 2592000)
#        cache.set(str(self.id)+"_pref", str(self.pref), 2592000)
#        super(Tab, self).save(*args, **kwargs)

    def delete(self):
        file_list = self.tabfile_set.all()
        for f in file_list:
            f.delete()
        super(Tab, self).delete()

    class Meta:

        ordering = ['pref']


class TabFile(models.Model):

    title = models.CharField(max_length=50)
    tab_file = \
        models.FileField(upload_to=upload_handler('Events/TabFiles'))
    tab = models.ForeignKey(Tab, blank=True, null=True)
    url = models.CharField(max_length=200)

    def delete(self):
        os.remove(self.tab_file.name)
        super(TabFile, self).delete()


class Question(models.Model):

    q_number = models.IntegerField(max_length=2)
    title = models.TextField(max_length=1500, blank=False)

    def __unicode__(self):
        return self.title

    class Meta:

        ordering = ['q_number']


class SubjectiveQuestion(Question):

    event = models.ForeignKey(Event)


class ObjectiveQuestion(Question):

    event = models.ForeignKey(Event)

    def delete(self):
        options = self.mcqoption_set.all()
        for option in options:
            option.delete()
        super(ObjectiveQuestion, self).delete()


class MCQOption(models.Model):

    question = models.ForeignKey(ObjectiveQuestion, null=True,
                                 blank=True)
    option = models.CharField(max_length=1)
    text = models.TextField(max_length=1000)

    def __unicode__(self):
        return self.text

    class Meta:

        ordering = ['option']


class MobAppTab(models.Model):

    event = models.OneToOneField(Event, blank=True, null=True)
    text = models.TextField()

class Sponsor(models.Model):
    """
    This model is for adding details about sponsors
    """
    name = models.CharField(max_length = 20,unique = True, help_text = 'Enter company name (Required)')
    index_number = models.IntegerField(blank = True, help_text = 'Indicates order of importance of sponsor - The most important sponsor will be index 1.')
    url = models.URLField(blank = True)
    logo = models.URLField(blank = True)
    year = models.IntegerField(default = "2013")
    about = models.CharField(max_length = 50, help_text = 'Type of sponsor')
    
    def __unicode__(self):
        return self.name
