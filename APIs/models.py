from django.db import models
from django.conf import settings
from datetime import datetime

EVENT_CATEGORIES = (
	("Aerofest", "Aerofest"),
	("Coding", "Coding"),
	("Design and Build", "Design and Build"),
	("Involve", "Involve"),
	("Quizzes", "Quizzes"),
	("Online", "Online"),
	("Department Flagship", "Department Flagship"),
	("Spotlight", "Spotlight"),
	("Workshops", "Workshops"),
    ("Others", "Others"),
)

CATEGORY = (
    ("Update", "Update"),
    ("Announcement", "Announcement"),
)

class Event(models.Model):
    title = models.CharField(max_length = 30)
    category = models.CharField(max_length=50,choices= EVENT_CATEGORIES)
    
    def __unicode__(self):
        return '%s' % self.title
    
    class Meta:
        db_table='events_event'

class Update(models.Model):
    description = models.TextField()
    category = models.CharField(max_length = 15, choices = CATEGORY, help_text='You can add 4 updates and 1 announcement. Mark as announcement only if the information is of highest importance')
    event = models.ForeignKey(Event, null=True, blank=True)
    expired = models.BooleanField(default=False, help_text='Mark an update/announcement as expired if it is no longer relevant or you have more than 4 updates (or 1 announcement) ')
    date = models.DateField(default=datetime.now)

    class Meta:
        db_table = 'events_update'

class MobAppTab(models.Model):
    event = models.ForeignKey(Event, blank=True, null=True)
    title = models.CharField(max_length=30)
    text = models.TextField()

    class Meta:
        db_table = 'events_tab'
