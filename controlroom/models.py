from django.db import models
from datetime                   import datetime, timedelta
from users.models import UserProfile

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

HOSTEL_CHOICES = (
    ('Alakananda','Alakananda'),
    ('Brahmaputra','Brahmaputra'),
    ('Cauvery','Cauvery'),
    ('Ganga','Ganga'),
    ('Godavari','Godavari'),
    ('Jamuna','Jamuna'),
    ('Krishna','Krishna'),
    ('Mahanadhi','Mahanadhi'),
    ('Mandakini','Mandakini'),
    ('Narmada','Narmada'),
    ('Pamba','Pamba'),
    ('Saraswathi','Saraswathi'),
    ('Sarayu','Sarayu'),
    ('Sharavati','Sharavati'),
    ('Sindhu','Sindhu'),    
    ('Tamraparani','Tamraparani'),   
    ('Tapti','Tapti'),   
    )

class AvailableRooms(models.Model):
    room_no = models.CharField(max_length = 20)
    hostel = models.CharField(max_length = 20, choices = HOSTEL_CHOICES)
    max_number = models.IntegerField()
    mattresses = models.IntegerField(default=0)
    already_checkedin = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s' % self.hostel + ',' + self.room_no

class IndividualCheckIn(models.Model):
    room = models.ForeignKey(AvailableRooms)
    duration_of_stay = models.IntegerField()
    number_of_mattresses_given = models.IntegerField(default = 0,blank = True)
    mattress_room = models.CharField(max_length = 20)
    shaastra_ID = models.CharField(max_length = 20)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    phone_no = models.CharField(max_length = 15)
    check_in_control_room = models.CharField(max_length = 20,choices = HOSTEL_CHOICES)
    check_out_control_room = models.CharField(max_length = 20,choices = HOSTEL_CHOICES, blank = True)
    check_in_date = models.DateTimeField(default = datetime.now)
    check_out_date = models.DateTimeField(null = True, blank=True) 
    comments = models.CharField(max_length = 1000, blank=True)
    
    def __unicode__(self):
        return self.first_name

    class Admin:
        pass

class BarcodeMap(models.Model):
    """
    Maps barcode to participant
    """
    barcode = models.CharField(max_length=128,blank=True)
    shaastra_id = models.ForeignKey(UserProfile, blank=True, null=True)  
    
    def __str__(self):
        return self.barcode

