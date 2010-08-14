DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'servertail',
        'USER': 'servertail',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

MEDIA_URL = 'http://servertail.com/media/'
ADMIN_MEDIA_PREFIX = 'http://servertail.com/media/admin/'

CACHE_BACKEND = 'newcache://127.0.0.1:11211/'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'