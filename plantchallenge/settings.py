# -*- coding: utf-8 -*-

"""
Django settings for testproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


DEBUG = True

TEMPLATE_DEBUG = DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'really secret key'

# Application definition

INSTALLED_APPS = (
    'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    # 'flatblocks',
    'lazysignup',
    'proso_ab',
    'proso_common',
    'proso_models',
    'proso_user',
    # 'proso_feedback',
    'proso_flashcards',
    'social_auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'proso_common.models.RequestMiddleware',
    'proso_ab.models.ABMiddleware',
    'proso_models.cache.RequestCacheMiddleware',
    'proso.django.log.RequestLogMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'proso_questions_client.middleware.AuthAlreadyAssociatedMiddleware',
)

ROOT_URLCONF = 'plantchallenge.urls'


DATABASES = {"default": dj_database_url.config(default='postgresql://proso_apps:proso_apps@localhost/plantchallenge')}

# Internationalization

USE_I18N = False

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


DATA_DIR = os.path.join(BASE_DIR, 'data')

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'), )


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'lazysignup.backends.LazySignupBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
)

FACEBOOK_APP_ID = os.getenv('PROSO_FACEBOOK_APP_ID', '')
FACEBOOK_API_SECRET = os.getenv('PROSO_FACEBOOK_API_SECRET', '')
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

SOCIAL_AUTH_CREATE_USERS = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_DEFAULT_USERNAME = 'socialauth_user'
LOGIN_ERROR_URL = '/login/error/'
SOCIAL_AUTH_ERROR_KEY = 'socialauth_error'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
GOOGLE_OAUTH2_CLIENT_ID = os.getenv('PROSO_GOOGLE_OAUTH2_CLIENT_ID', '')
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv('PROSO_GOOGLE_OAUTH2_CLIENT_SECRET', '')

# http://stackoverflow.com/questions/22005841/is-not-json-serializable-django-social-auth-facebook-login
SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'


ALLOWED_HOSTS = ["*"]

LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_UID_LENGTH = 222
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 200
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 135
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 125


PROSO_PREDICTIVE_MODEL = 'proso.models.prediction.PriorCurrentPredictiveModel'
PROSO_ENVIRONMENT = 'proso_models.models.DatabaseEnvironment'
PROSO_ITEM_SELECTION = 'proso.models.item_selection.ScoreItemSelection'
PROSO_OPTION_SELECTION = 'proso.models.option_selection.NonOptionSelection'
PROSO_FLASHCARDS_OPTION_SET = 'proso_flashcards.flashcard_construction.ContextOptionSet'
PROSO_FLASHCARDS_DIRECTION = 'proso_flashcards.flashcard_construction.RandomDirection'
PROSO_FLASHCARDS = {}


EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'request': {
            'level': 'DEBUG',
            'class': 'proso.django.log.RequestHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s "%(message)s"'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'request'],
            'propagate': True,
            'level': 'DEBUG'
        }
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}