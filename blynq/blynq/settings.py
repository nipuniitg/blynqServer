"""
Django settings for blynq project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1ig8fo2929x)i=c7k$z0qe#@1n())0o2rt7*45^j^td5_duj$m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['http://www.blynq.in', 'www.blynq.in', 'blynq.in']


# Application definition

INSTALLED_APPS = (
    'django_pdb',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djng', # django-angular http://django-angular.readthedocs.org/en/latest/installation.html
    'schedule', # https://github.com/llazzaro/django-scheduler
    'reversion',    # http://django-reversion.readthedocs.io/en/latest/
    'coverage',
    'authentication',
    'screenManagement',
    'contentManagement',
    'playlistManagement',
    'playerManagement',
    'scheduleManagement',
    #'django_js_reverse',
)

MIDDLEWARE_CLASSES = (
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_pdb.middleware.PdbMiddleware',
    'customLibrary.app_exceptions.AppExceptionTrap',
)

ROOT_URLCONF = 'blynq.urls'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blynq.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Blynq_DB_DEV',
        'USER': 'blynq',
        'PASSWORD': 'Believe',
        'HOST': '127.0.0.1',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
# Upload app specific images into /static/appName/image1.jpg

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

# Media files directory takes care of the uploaded pictures
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# The below variables are for registration app
# REGISTRATION_OPEN = True        # If True, users can register
# ACCOUNT_ACTIVATION_DAYS = 7     # One-week activation window; you may, of course, use a different value.
# REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logged in.
# LOGIN_REDIRECT_URL = '/admin/'  # The page you want users to arrive at after they successful log in
LOGIN_URL = '/authentication/login/'  # The page users are directed to if they are not logged in,

# Content related settings
DEFAULT_DISPLAY_TIME = 10
STORAGE_LIMIT_PER_ORGANIZATION = 5*1024*1024*1024  # 1 gb 1*1024*1024*1024


LOG_DIRECTORY = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'debug': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIRECTORY, 'debug.log'),
        },
    },
    'loggers': {
        'consoleLog': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
        'django.request': {
            'handlers': ['debug'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'debugFileLog': {
            'handlers': ['debug'],
            'propagate': True,
        }
    },
}


if DEBUG:
    MEDIA_HOST = 'http://127.0.0.1:8000'
    USERCONTENT_DIR = 'test_usercontent'
    DELETED_CONTENT_DIR = 'test_deletedcontent'
else:
    MEDIA_HOST = 'http://www.blynq.in'
    USERCONTENT_DIR = 'usercontent'
    DELETED_CONTENT_DIR = 'deletedcontent'

PLAYER_UPDATES_DIR = 'player_updates'

# in MEDIA_ROOT
# the uploaded content of each user is present in /media/usercontent/userdetails.user.id/
# the deleted files are moved to /media/deletedcontent/organization.organization_id



EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'django@blynq.in'
EMAIL_HOST_PASSWORD = 'Asdf;lkj'
