from webapp.settings.common import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': 'webapp_prod',
        'USER': 'webapp',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
