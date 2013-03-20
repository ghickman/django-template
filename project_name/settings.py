# Django settings for {{ project_name }} project.
import mimetypes
import os

from django.core.urlresolvers import reverse_lazy
import django_cache_url
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.join(BASE_DIR, os.path.pardir)

DEBUG = bool(os.environ.get('DEBUG', False))

DATABASES = {'default': dj_database_url.config(default='postgres://localhost/{{ project_name }}')}

CACHES = {'default': django_cache_url.config(default='memcached://127.0.0.1:11211')}

ADMINS = (('Admin', 'george@ghickman.co.uk'),)
ADMIN_EMAILS = zip(*ADMINS)[1]
EMAIL_SUBJECT_PREFIX = '[{{ project_name }}] '
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

TIME_ZONE = 'UTC'
USE_L10N = True  # Locale
USE_TZ = True

LANGUAGE_CODE = 'en-GB'
USE_I18N = False  # Internationalization

# AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_LOCATION = os.environ.get('AWS_LOCATION', '')
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '{{ project_name }}')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
AWS_CLOUDFRONT_STREAMING_DOMAIN = os.environ.get('AWS_CLOUDFRONT_STREAMING_DOMAIN')
STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE', 'storages.backends.s3boto.S3BotoStorage')
S3_URL = 'http://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

# Static
MEDIA_ROOT = os.path.join(ROOT_DIR, 'client_media')
MEDIA_URL = '/client_media/'
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (STATICFILES_DIR,)
STATIC_ROOT = os.path.join(ROOT_DIR, 'static_media')
STATIC_URL = os.environ.get('STATIC_URL', S3_URL + 'static/')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

mimetypes.add_type('text/x-component', '.htc')

TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'admin_sso.auth.DjangoSSOAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = reverse_lazy('auth_login')
LOGOUT_URL = reverse_lazy('auth_logout')
LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = '{{ project_name }}.urls'
SECRET_KEY = '{{ secret_key }}'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SITE_ID = 1
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

INSTALLED_APPS = (
    # Project Apps
    '{{ project_name }}',

    # Libraries
    'admin_sso',
    'debug_toolbar',
    'django_extensions',
    'gunicorn',
    'raven.contrib.django',
    'south',

    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}
    },
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['sentry', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'default': {
            'handlers': ['sentry', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'sentry.errors': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propogate': True,
        },
    }
}

# Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
INTERNAL_IPS = ('127.0.0.1',)
