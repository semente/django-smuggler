from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url, include

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/login/$', admin.site.login,
        name='login', prefix='admin'),  # for Django < 1.7
    url(r'^admin/', include(admin.site.urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
