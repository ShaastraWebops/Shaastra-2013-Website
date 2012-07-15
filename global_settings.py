import os

TIME_ZONE = 'Asia/Calcutta'
LANGUAGE_CODE = 'en-us'


# settings that will be common and useful.
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR_NAME = PROJECT_DIR.split('/')[-1] # used in dajaxice.[my_project_folder_name].events.[ajax_function] (see context_processors.py)
AJAX_TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates/events', 'ajax') # path where ajax templates are stored


SITE_ID = 1

USE_I18N = False

USE_L10N = True

AUTH_PROFILE_MODULE = 'users.UserProfile'

FACEBOOK_APP_ID = '291744470918252'
FACEBOOK_APP_SECRET = '599f13aad496d3acc8ea887a0e889b92'
FACEBOOK_SCOPE = 'email'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'admin',
    'core',
    'coord',
    'users',
    'events',
    'submissions',
    'dtvpicker',
    'dajaxice',
    'dajax', 
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.request",
"django.contrib.messages.context_processors.messages",
"context_processors.site_url",)

DAJAX_JS_FRAMEWORK = "jQuery"
DAJAX_MEDIA_PREFIX='dajax'
DAJAXICE_MEDIA_PREFIX="dajaxice"
DAJAXICE_DEBUG = True

EMAIL_HOST='localhost'
#Default: 'localhost'
#The host to use for sending e-mail.
EMAIL_HOST_PASSWORD='$#aastra20iiw3b0ps'
#Default: '' (Empty string)
EMAIL_HOST_USER='shaastra'

