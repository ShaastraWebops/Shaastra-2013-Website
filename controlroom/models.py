from django.db import models
from datetime                   import datetime, timedelta

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

HOSTEL_CHOICES = (
    ('Alakananda','Alakananda'),
    ('Ganga','Ganga'),
    ('Jamuna','Jamuna'),
    ('Mahanadhi','Mahanadhi'),
    ('Mandakini','Mandakini'),
    ('Pamba','Pamba'),
    ('Sindhu','Sindhu'),    
    ('Tamraparani','Tamraparani'),
    ('Sarayu','Sarayu'),
    ('Sarayu Extn','Sarayu Extn'),
    ('C-2-8','C-2-8'),
    ('Sharavati','Sharavati'),   
    )

CONTROL_ROOM_CHOICES = (
    ('Ganga','Ganga'),
    ('Sharavati','Sharavati'),
    )

MATTRESS_CHOICES = (
    ('Ganga','Ganga'),
    ('Sindhu','Sindhu'),
    ('Tamraparani','Tamraparani'),
    ('Jamuna','Jamuna'),
    ('Sharavati','Sharavati'),
    ('Sarayu Extn','Sarayu Extn'),
    )

class AvailableRooms(models.Model):
    room_no = models.CharField(max_length=20)
    hostel = models.CharField(max_length = 20, choices = HOSTEL_CHOICES)
    max_number = models.IntegerField()
    mattresses = models.IntegerField(default=0)
    already_checkedin = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s' % self.hostel + ',' + self.room_no

class IndividualCheckIn(models.Model):
    room = models.ForeignKey(AvailableRooms)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              default='F')
    duration_of_stay = models.IntegerField()
    number_of_mattresses_given = models.IntegerField(default = 0,blank = True)
    mattress_room = models.CharField(max_length = 20, choices = MATTRESS_CHOICES)
    shaastra_ID = models.CharField(max_length = 20)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    phone_no = models.CharField(max_length = 15)
    check_in_control_room = models.CharField(max_length = 20,choices = CONTROL_ROOM_CHOICES)
    check_out_control_room = models.CharField(max_length = 20,choices = CONTROL_ROOM_CHOICES, blank = True)
    check_in_date = models.DateTimeField(default = datetime.now)
    check_out_date = models.DateTimeField(null = True, blank=True) 
    comments = models.CharField(max_length = 1000, blank=True)
    
    def __unicode__(self):
        return self.first_name

    class Admin:
        pass

class Mattresses(models.Model):
    team_leader_id = models.CharField(max_length = 20)
    no_of_mattresses = models.IntegerField(default = 0,blank = True)


