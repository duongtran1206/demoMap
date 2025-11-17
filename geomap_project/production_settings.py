from .settings import *
import os

# Production settings
DEBUG = False
ALLOWED_HOSTS = ['*']  # Allow all hosts for flexibility

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'ALLOWALL'

# CORS settings for production
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Database - use file-based SQLite for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/demoMap/django.log',
        },
    },
    'root': {
        'handlers': ['file'],
    },
}