from webapp.settings.common import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

def custom_show_toolbar(request):
    return False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'INTERCEPT_REDIRECTS': False,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'webapp_dev',
        'USER': 'webapp',
        'PASSWORD': '0F.jz842011',
        'HOST': '',
        'PORT': '',
    }
}

