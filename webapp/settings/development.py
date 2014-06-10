from webapp.settings.common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATIC_URL = '/static/'

import sys
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }
