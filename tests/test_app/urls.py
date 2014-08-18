from django.contrib import admin
from django.conf.urls import patterns, url, include

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include('smuggler.urls')),
                       url(r'^admin/', include(admin.site.urls)),)
