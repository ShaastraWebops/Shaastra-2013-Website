#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from models import SubEvent, Venue, VenueGroupAlias
from django.forms import ModelForm


class SubEventForm(ModelForm):

    class Meta:

        model = SubEvent
        fields = ('title', 'event', 'start_date_and_time', 'end_date_and_time', 'venue')
        widgets = {
            'event' : forms.HiddenInput(),  # The event field should be populated automatically depending on which coord requests the form.
        }
        
    def checkSubEventDTVClash(self, venuesChosenList, startChosen, endChosen):
        """
        Checks if the sub-event submitted clashes with any other sub-event (under any event) in the database.
        If they do clash, returns an error message that describes the venue and its booking time.
        """
        '''
        Logic:: How to check if two sub-events (say A and B) clash:
            if A.venue and B.venue are disjoint sets:
                They don't clash
            elif A.start > B.end:
                They don't clash
            elif A.end < B.start:
                They don't clash
            else:
                They clash
        '''
        
        subEventList = SubEvent.objects.all()
        if self.instance:  # Excludes the "self" record if it is being updated.
            subEventList = subEventList.exclude(id = self.instance.id)        
            
        subEventDTVClashMsgs = []
        
        for subEvent in subEventList:
            if not (subEvent.start_date_and_time and subEvent.end_date_and_time and subEvent.venue):
                continue
                
            for venue in venuesChosenList:
                
                if venue not in subEvent.venue.all():
                    continue  # No clash

                if subEvent.start_date_and_time >= endChosen:  # Start date-time of subEvent is after end date-time of self
                    continue  # No clash

                if subEvent.end_date_and_time <= startChosen:  # End date-time of subEvent is before start date-time of self
                    continue  # No clash
            
                # The events clash.
                # Must tell user from when to when the venue is booked.
                subEventDTVClashMsgs.append(u'%s is booked by %s (%s) from %s to %s.' % (venue, 
                                                                                   subEvent.event.title,
                                                                                   subEvent.title,
                                                                                   subEvent.start_date_and_time, 
                                                                                   subEvent.end_date_and_time))

        if subEventDTVClashMsgs:
            return subEventDTVClashMsgs
        return None

    def clean(self):
        """
        This method will work to clean the instance of SubEvent created.
        Validations to be performed:
            * The sub-event's title must be unique under it's event.
            * The seconds and micro-seconds parameters of the start and end times must be zero (if not, set them).
            * The start of the sub-event must not be after the end.
            * The start of the sub-event cannot be the same as the end.
            * All venue validation must be done after saving the model instance. Validations to be performed:
                * The venues chosen must be in the same block.
                * The DTV of the sub-event must not clash with any other sub-event's DTV.
                    ~ The check for this is defined in the checkSubEventDTVClash() method.
            * The last_modified field must be updated to the current date and time.
        """
        # References:
        # http://stackoverflow.com/questions/3853657/django-manytomany-validation
        # https://docs.djangoproject.com/en/dev/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
        # http://stackoverflow.com/questions/2117048/django-overriding-the-clean-method-in-forms-question-about-raising-errors
        
        errors = []

        super(SubEventForm, self).clean()  # Calling clean method of the super class
        
        # Get all attributes of the SubEvent POSTed:
        title = self.cleaned_data.get('title', None)
        event = self.cleaned_data.get('event', None)
        start_date_and_time = self.cleaned_data.get('start_date_and_time', None)
        end_date_and_time = self.cleaned_data.get('end_date_and_time', None)
        venue = self.cleaned_data.get('venue', None)

        # The sub-event's title must be unique under its event.
        if title is not None:

            subEventList = SubEvent.objects.filter(event = event)
            if self.instance:
                subEventList = subEventList.exclude(id = self.instance.id)
            
            for subEvent in subEventList:
                if subEvent.title == title:
                    errors.append(u'You already have a sub-event with the name "%s".' % subEvent.title)
                    break
        
        # The start and end times must not contain seconds and micro-seconds: Reset them to 0.
        if start_date_and_time:
            start_date_and_time = start_date_and_time.replace(second = 0, microsecond = 0)
        if end_date_and_time:
            end_date_and_time = end_date_and_time.replace(second = 0, microsecond = 0)
            
        # The start of the sub-event must not be after the end.
        # The start of the sub-event cannot be the same as the end
        if start_date_and_time and end_date_and_time:
            # Ensures that both these fields are valid
            if start_date_and_time > end_date_and_time:
                errors.append(u'Surely the event cannot start after it has ended!')
            elif start_date_and_time == end_date_and_time:
                errors.append(u'Surely the start and end time cannot be the same!')
                
        # The venues chosen must be in the same block
        if venue:
            blockList = [v.block for v in venue.all()]
            blockList = list(set(blockList))  # Converting the blockList to a set removes the duplicates. Then convert it back to a list.
            if len(blockList) > 1:  # If there is more than one block now, then they are distinct and this is an error.
                errors.append(u'You have selected venues from more than one block. You are not allowed to have venues so far apart.')
                    
        # The DTV of the sub-event must not clash with any other sub-event's DTV.
        if venue and start_date_and_time and end_date_and_time:
            # Ensures that venue is present
            # Already checked validity of start and end dates and times
            subEventDTVClashErrorMsgs = self.checkSubEventDTVClash(venue.all(), start_date_and_time, end_date_and_time)
            if subEventDTVClashErrorMsgs is not None:
                errors.extend(subEventDTVClashErrorMsgs)
    
        if errors:
            raise forms.ValidationError(errors)
        return self.cleaned_data
        
class EventUnlockForm(forms.Form):
    unlock_reason = forms.CharField(max_length = 1024, help_text = 'Please give reason for unlocking.')
    
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        
class VenueGroupAliasForm(ModelForm):
    class Meta:
        model = VenueGroupAlias
    #TODO(Anant): Add logic here to ensure that there is only one alias for a particular venue set.

