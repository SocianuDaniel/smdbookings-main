from .base import *

ALLOWED_HOSTS = ['mysite.com',]
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'smd',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}
STATIC_ROOT = 'STATICFILES'
try:
    from .local import *
except ImportError:
    pass