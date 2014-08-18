DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'smuggler.db'
    }
}

SECRET_KEY = 'mAtTzVPOV9JY4eJQfqgW8eAS9DWKnt3MkvvpQI2MzkhAz7z3'

INSTALLED_APPS = [
    'django.contrib.sites',
    'smuggler',
    'test_app',
]
