# Haystack settings for running tests.
DATABASE_ENGINE = 'django.db.backends.sqlite3'
DATABASE_NAME = 'smuggler.db'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'smuggler.db'
    }
}

SECRET_KEY = 'mAtTzVPOV9JY4eJQfqgW8eAS9DWKnt3MkvvpQI2MzkhAz7z3'

INSTALLED_APPS = [
    'smuggler',
    'test_app',
]
