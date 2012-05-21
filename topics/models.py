from django.db import models

# Create your models here.

class Topic(models.Model):
	title=models.CharField(max_length=500)
	url_name=models.CharField(max_length=500)
	information=models.TextField(max_length=2000)
	index_number=models.IntegerField()
	def __unicode__(self):
		return self.title
	class Meta:
		ordering=['index_number']

class TopicImage(models.Model):
	name=models.CharField(max_length=75,blank=True)
	image=models.ImageField(upload_to='topic',null=True,blank=True)
	topic=models.ForeignKey(Topic,related_name='topicimage')
	def __unicode__(self):
		return self.name

	
