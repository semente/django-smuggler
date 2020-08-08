from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.autodiscover()

urlpatterns = [
    path('admin/', include('smuggler.urls')),
    path('admin/', admin.site.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
