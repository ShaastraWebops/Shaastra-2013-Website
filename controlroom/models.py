from django.db import models
from datetime                   import datetime, timedelta

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
    already_checkedin = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s' % self.room_no + ',' + self.hostel

class IndividualCheckIn(models.Model):
    room = models.ForeignKey(AvailableRooms)
    shaastra_ID = models.CharField(max_length = 20)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    phone_no = models.CharField(max_length = 15)
    check_in_control_room = models.CharField(max_length = 20,choices = HOSTEL_CHOICES)
    check_out_control_room = models.CharField(max_length = 20,choices = HOSTEL_CHOICES, blank = True)
    check_in_date = models.DateTimeField(default = datetime.now)
    check_out_date = models.DateTimeField(null = True, blank=True) 
    comments = models.CharField(max_length = 1000, blank=True)

