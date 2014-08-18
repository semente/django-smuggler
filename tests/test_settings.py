DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'smuggler.db'
    }
}

SECRET_KEY = 'mAtTzVPOV9JY4eJQfqgW8eAS9DWKnt3MkvvpQI2MzkhAz7z3'

ROOT_URLCONF = 'test_app.urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'smuggler',
    'test_app',
]
