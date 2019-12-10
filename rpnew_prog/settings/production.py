import os
import json
from django.core.exceptions import ImproperlyConfigured
from .base import *

with open(os.path.join(PROJECT_DIR, 'settings/secrets.json')) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    '''Get the secret variable or return explicit exception.
    Thanks to twoscoopsofdjango'''
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)

DEBUG = False

ALLOWED_HOSTS = [
    'rifondazionepodistica.it',
    'www.rifondazionepodistica.it',
]

WSGI_APPLICATION = 'rpnew_prog.wsgi_prod.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST': get_secret('HOST'),
        'PORT': get_secret('PORT'),
    }
}

#control if you can use same keys as staging
RECAPTCHA_PUBLIC_KEY = get_secret('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = get_secret('RECAPTCHA_PRIVATE_KEY')

# Mail configuration
# https://docs.webfaction.com/software/django/config.html#configuring-django-to-send-mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'no-reply@rifondazionepodistica.it'
SERVER_EMAIL = 'no-reply@rifondazionepodistica.it'

STATIC_ROOT = '/home/apperilli/webapps/rpteststatic/'
STATIC_URL = 'https://rifondazionepodistica.it/static/'

MEDIA_ROOT = '/home/apperilli/webapps/rpteststatic/media/'
MEDIA_URL = 'https://rifondazionepodistica.it/static/media/'

SECRET_KEY = get_secret('SECRET_KEY')

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'https://rifondazionepodistica.it'

try:
    from .local import *
except ImportError:
    pass
