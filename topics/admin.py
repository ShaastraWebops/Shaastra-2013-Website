from django.contrib import admin
from topics.models import *

"""
This is similar to the admin.py in the app
shaastra_events.
""" 

class TopicImageInline(admin.TabularInline):
	model=TopicImage
	extra=1

class TopicAdmin(admin.ModelAdmin):
	inlines=[TopicImageInline]
	fields=['title','index_number','information']
	def save_model(self, request, obj, form, change):
		obj.url_name = obj.title.replace(" ","").replace('!', '').replace('&', '').replace("'", '').replace('-', '').replace("?",'')
		obj.save()


admin.site.register(Topic,TopicAdmin)

