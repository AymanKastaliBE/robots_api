from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include(('ata_api.urls', 'ata_api'), namespace='ata_api')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('authentication/', include(('auth_api.urls', 'auth_api'), namespace='auth_api')),
    path('api/', include(('gdrfad_api.urls', 'gdrfad_api'), namespace='gdrfad_api')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
