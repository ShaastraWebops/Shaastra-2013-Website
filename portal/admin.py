from portal.models import *
from django import forms
from django.forms import *
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import *
from django.template import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
"""
The following custom GroupAdmin is to exclude unnecessary permissions on display
"""
class MyGroupAdmin(GroupAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(MyGroupAdmin, self).get_form(request, obj, **kwargs) # Get form from original GroupAdmin.
        permissions = form.base_fields['permissions']
        permissions.queryset = permissions.queryset.filter(content_type__app_label__in=['portal'])
        #To exclude just a single permission use content_type__name
        #permissions.queryset = permissions.queryset.exclude(content_type__name='permission')
        return form

"""
The following custom UserAdmin is to exclude unnecessary columns on display
"""
class MyUserAdmin(UserAdmin):
    #normally staff status is also displayed, but since all are staff, there is no need
    list_display = ['username','email','first_name','last_name']
    #makes more sense to filter by group than the default "kind of user"
    list_filter = ['groups',]
    """
    A very stupid way of ensuring that user permissions is not visible
    to admin so that there is no confusion.
    """
    def get_readonly_fields(self, request, obj=None):
        fields = ('is_active','user_permissions','is_staff')
        return fields
        
    """
    To save all users as staff by default so that they can login
    """    
    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        obj.save()        
"""
There is no necessity for Site to be on
the spons admin site.
"""
admin.site.unregister(Site)

"""
In urls.py, admin.site.urls is included.
This looks for admin.py in the application as
indicated by INSTALLED_APPS. Executes the code.
By default django.contrib.auth has admin.py.
This is the reason, User and Group is available
on the admin site.

"""
"""
Inline is when there is a ForeignKey to a 
certain class, then we must be able to add
many instances of that class efficiently. 
The Inline will be based on the class
specified in 'model' and 'extra' specifies
the number of extra fields that will be
displayed when you add/edit
Options for inline editing can be found in
django.contrib.admin.options
"""
class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1   
    
class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 1
    
class EventInline(admin.TabularInline):
    model = Event
    extra=1
        
    
"""
The corresponding class in Admin is for adding
actions, display columns, search fields, filter,
etc. all specific to Admin site.
"""

class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryImageInline,EventInline]
    fields = ['name']
    list_display = ['name','get_events']
        
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        This overrides the default save_model available
        in django/contrib/admin/options.py
        This has been added because special characters
        cannot be passed into url
        """
        obj.url_name = obj.name.replace(" ","_").replace('!', '').replace('&', '').replace("'", '').replace('-', '').replace("?",'')
        obj.save()
        

class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageInline]
    list_display = ['title','category','status']
    search_fields = ['title','category__name']
    actions = ['make_sold', 'make_available','count_sold']
    
    """
    The following actions can be found on the admin
    site. When certain objects are selected by 
    selecting through checkbox, they form the queryset.
    Functions like count and filter are available
    as usual for the queryset. 
    """
    def make_sold(self, request, queryset):
	"""
	This enables one to change the status of several events at once
	by selecting their respective check boxes and performing the action make sold
	"""
        updated = queryset.update(status='s')
        if updated == 1:
            message = "1 event was"
        else:
            message = "%s events were" % updated
        self.message_user(request, "%s successfully markedfieldsets as sold." % message)
        
    def make_available(self, request, queryset):
	"""
	This enables one to change the status of several events at once
	by selecting their respective check boxes and performing the action make sold
	"""
        updated = queryset.update(status='a')
        if updated == 1:
            message = "1 event was"
        else:
            message = "%s events were" % updated
        self.message_user(request, "%s successfully marked as available." % message)
        
    def count_sold(self, request, queryset):
	"""
	This is to count the number of events sold
	"""
        filtered = queryset.filter(status='s')
        counted = filtered.count()
        if counted == 1:
            message = "1 event is"
        else:
            message = "%s events are" % counted
        self.message_user(request, "%s sold." % message)       


class TopicImageInline(admin.TabularInline):
	model=TopicImage
	extra=1

class TopicAdmin(admin.ModelAdmin):
    """
    Field 'information' is not displayed in admin site. Check forms.py
    for custom form for 'information'
    """
	inlines=[TopicImageInline]
	list_display = ['index_number','title',]
	fields=['title','index_number']
	def save_model(self, request, obj, form, change):
		obj.url_name = obj.title.replace(" ","_").replace('!', '').replace('&', '').replace("'", '').replace('-', '').replace("?",'')
		obj.save()

class PreviousSponsorAdmin(admin.ModelAdmin):
    list_display = ['name']
    
"""
Only those classes explicitly registered will
be displayed.
"""
admin.site.unregister(Group)  # You must unregister first
admin.site.register(Group, MyGroupAdmin)
admin.site.unregister(User)  # You must unregister first
admin.site.register(User, MyUserAdmin)

admin.site.register(PreviousSponsor, PreviousSponsorAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
