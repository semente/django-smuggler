from django.contrib import admin
from django.conf.urls import patterns, url, include

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include('smuggler.urls')),
                       url(r'^admin/login/$', admin.site.login,
                           name='login', prefix='admin'),  # for Django < 1.7
                       url(r'^admin/', include(admin.site.urls)),)
