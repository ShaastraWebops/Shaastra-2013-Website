#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from events.models import Event

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu And Kashmir', 'Jammu And Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Orissa', 'Orissa'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman And Nicobar Islands', 'Andaman And Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra And Nagar Haveli', 'Dadra And Nagar Haveli'),
    ('Daman And Diu', 'Daman And Diu'),
    ('Lakshadweep', 'Lakshadweep'),
    ('NCT/Delhi', 'NCT/Delhi'),
    ('Puducherry', 'Puducherry'),
    ('Outside India', 'Outside India'),
    )


class College(models.Model):

    name = models.CharField(max_length=255,
                            help_text='The name of your college. Please refrain from using short forms.'
                            )
    city = models.CharField(max_length=30,
                            help_text='The name of the city where your college is located. Please refrain from using short forms.'
                            )
    state = models.CharField(max_length=40, choices=STATE_CHOICES,
                             help_text='The state where your college is located. Select from the drop down list'
                             )

    def __unicode__(self):
        return '%s, %s, %s' % (self.name, self.city, self.state)

    class Admin:

        pass


# User profile common to all users

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              default='F')  # Defaults to 'girl' ;-)
    age = models.IntegerField(default=18)
                              # help_text='You need to be over 12 and under 80 years of age to participate'
                              # No age limit now.
    branch = models.CharField(max_length=50, blank=True, null=True,
                              help_text='Your branch of study')
    mobile_number = models.CharField(max_length=15, blank=True, null=True,
            help_text='Please enter your current mobile number')
    college = models.ForeignKey(College, null=True, blank=True)
    college_roll = models.CharField(max_length=40, null=True)

    shaastra_id = models.CharField(max_length = 20, unique = True, null=True)

    activation_key = models.CharField(max_length=40, null=True)
    key_expires = models.DateTimeField(null=True)
    want_accomodation = models.BooleanField(default=False, help_text = "This doesn't guarantee accommodation during Shaastra.")
    is_core = models.BooleanField(default=False)
    is_hospi = models.BooleanField(default=False)

#    is_coord        = models.BooleanField....(default = False)

    is_coord_of = models.ForeignKey(Event, null=True)

#    registered      = models.ManyToManyField(Event, null=True, related_name='registered_users')        #Events which this user has registered for

    facebook_id = models.CharField(max_length=20)
    access_token = models.CharField(max_length=250)
    registered_events = models.ManyToManyField(Event,
            related_name='participants', null=True)

    def __unicode__(self):
        return self.user.first_name

    class Admin:

        pass

class Team(models.Model):
    name            = models.CharField(max_length = 50)
    event           = models.ForeignKey(Event, null = False)
    leader          = models.ForeignKey(User, related_name = 'own_teams', blank = False, null = False)
    members         = models.ManyToManyField(User, related_name = 'joined_teams', blank = True, null = True)
    
    def __unicode__(self):
        return self.name
    '''
    class Meta:
        unique_together('name', 'event', )
    '''
