from .base import *

# Import the appropriate settings based on environment
import os

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'project.settings.production':
    from .production import *
else:
    from .development import *