from base import *


DEBUG = True
TEMPLATE_DEBUG = True

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
