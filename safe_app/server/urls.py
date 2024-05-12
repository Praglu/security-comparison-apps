from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('secret-admin/', admin.site.urls),
    path('', include('server.user.urls')),
    path('auth/', include('server.user.auth_urls')),
    path('transfer/', include('server.transfer.urls')),
    path('official/', include('server.official.urls')),
]
