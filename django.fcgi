#!/home/shaastra/bin/python
import sys, os

# Remove the "test" path, lest it gets confused
sys.path.insert(0, "/home/shaastra/django-projects/Shaastra-2013-Website")

sys.path.insert(0, "/home/shaastra/django-projects/Shaastra-2013-Website/login_register_forums")
sys.path.insert(0, "/home/shaastra/installation_files_django/flup")
sys.path.insert(0, 
'/home/shaastra/lib/python2.6/site-packages/flup-1.0.2-py2.6.egg')

# Switch to the directory of your project. (Optional)
os.chdir("/home/shaastra/django-projects/Shaastra-2013-Website/login_register_forums")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "login_register_forums.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

