from base import *


DEBUG = True
TEMPLATE_DEBUG = True
HOST_DOMAIN = 'localhost:8000'
USE_HTTPS = False


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
