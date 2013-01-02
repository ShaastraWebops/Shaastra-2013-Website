from django.db import models
from events.models import Event

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

class Participant(models.Model):
    """
    The participant's data.
    """
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              default='F')
    age = models.IntegerField(default=18)
    branch = models.CharField(max_length=50, blank=True, null=True,
                              help_text='Your branch of study')
    mobile_number = models.CharField(max_length=15, null=True,
            help_text='Please enter your current mobile number')
    college = models.CharField(max_length=100)
    college_roll = models.CharField(max_length=40, null=True)
    shaastra_id = models.CharField(max_length=30, blank=True)
    events = models.ManyToManyField(Event,
            related_name='participant', null=True)
    
    def __str__(self):
        return self.shaastra_id

# Create your models here.
class BarcodeMap(models.Model):
    """
    Maps barcode to participant
    """
    barcode = models.CharField(max_length=128,blank=True)
    shaastra_id = models.ForeignKey(Participant, blank=True, null=True)  
    
    def __str__(self):
        return self.barcode

