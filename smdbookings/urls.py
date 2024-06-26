"""
URL configuration for the  project.


"""
from django.contrib import admin
from django.urls import path, include

from base import urls as base_urls
from location import urls as location_urls
from users import urls as user_urls
from orari import urls as orari_urls
from turno import urls as turno_urls
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(base_urls)),

    path('users/', include(user_urls)),
    path('location/', include(location_urls)),
    path('location/orari/', include(orari_urls)),
    path('location/turno/', include(turno_urls)),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
