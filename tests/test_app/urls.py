from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url, include
import django
from distutils.version import StrictVersion
admin.autodiscover()

extra_url_kwargs = {'prefix': 'admin'} \
    if StrictVersion(django.get_version()) < StrictVersion('1.7')\
    else\
    {}
urlpatterns = [
    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/login/$', admin.site.login,
        name='login', **extra_url_kwargs),  # for Django < 1.7
    url(r'^admin/', include(admin.site.urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
