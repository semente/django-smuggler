from django.conf.urls import patterns, url, include

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'smuggler.db'
    }
}

SECRET_KEY = 'mAtTzVPOV9JY4eJQfqgW8eAS9DWKnt3MkvvpQI2MzkhAz7z3'

ROOT_URLCONF = patterns('',
                        url('^admin/', include('smuggler.urls')))

INSTALLED_APPS = [
    'django.contrib.sites',
    'smuggler',
    'test_app',
]
