from portal.models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import *
from django.template import *


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
Inline is when there is a ForeignKey
to a certain class, then we must be
able to add many instances of that
class efficiently.
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
        in django/contrib/options.py
        """
        obj.url_name = obj.name.replace(" ","_").replace('!', '').replace('&', '').replace("'", '').replace('-', '')
        obj.save()
        
"""
The following lines of code was an attempt to ensure
that event images can be added along with the event
when adding a category. However there is an error,
at class AddImageForm. In def __init__ in 
super(AddImageForm,self), the error displayed is
global name AddImageForm is not defined.
"""        
"""        
    def response_add(self, request, obj, post_url_continue='../%s/'):
        #response_add overrides the predefined one. Works at present only for add category, not change
        super(CategoryAdmin, self).response_add(request, obj, post_url_continue)
        return self.add_photos(request, obj)
        
    def add_photos(self, request, obj):
        current_category = Category.objects.get(name = obj)
        if 'save' in request.POST:
            form = self.AddImageForm(request.POST)
        else:
            form = self.AddImageForm()    
        return render_to_response('addimages.html',locals(),context_instance=RequestContext(request))

    class AddImageForm(forms.Form):
        event = forms.ModelChoiceField(Event.objects.all())
        photo = forms.ImageField(required=False)

        def __init__(self,qs,*args,**kwargs):
            super(AddImageForm, self).__init__(*args,**kwargs)
            self.fields['event'].queryset = qs   
"""    
class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageInline]
    list_display = ['title','category','status']
    search_fields = ['title','category__name']
    actions = ['make_sold', 'make_available','count_sold']
    
    def make_sold(self, request, queryset):
        updated = queryset.update(status='s')
        if updated == 1:
            message = "1 event was"
        else:
            message = "%s events were" % updated
        self.message_user(request, "%s successfully markedfieldsets as sold." % message)
        
    def make_available(self, request, queryset):
        updated = queryset.update(status='a')
        if updated == 1:
            message = "1 event was"
        else:
            message = "%s events were" % updated
        self.message_user(request, "%s successfully marked as available." % message)
        
    def count_sold(self, request, queryset):
        filtered = queryset.filter(status='s')
        counted = filtered.count()
        if counted == 1:
            message = "1 event is"
        else:
            message = "%s events are" % counted
        self.message_user(request, "%s sold." % message)       
"""
Only those classes explicitly registered will
be displayed.
"""

admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
