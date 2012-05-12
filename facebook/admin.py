from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import FacebookProfile

# We want to display our facebook profile, not the default user
admin.site.unregister(User)

class FacebookProfileInline(admin.StackedInline):
    model = FacebookProfile

class FacebookProfileAdmin(UserAdmin):
    inlines = [FacebookProfileInline]

admin.site.register(User, FacebookProfileAdmin)
