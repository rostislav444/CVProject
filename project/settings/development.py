from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-t&1ngzu5sxd&&j2ro+3n*@w(3(rf#55%el7e@24w9s4#m3b1_j"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Use SQLite for development if needed
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Use console email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


INTERNAL_IPS = [
    "127.0.0.1",
]
