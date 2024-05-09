from django.urls import path

from server.user import views
from server.user.auth import ApiObtainAuthTokenView, ApiRemoveAuthTokenView


auth_urlpatterns = [
    path('obtain-token', ApiObtainAuthTokenView.as_view(), name='obtain_auth_token'),
    path('remove-token', ApiRemoveAuthTokenView.as_view(), name='remove_auth_token'),
]


urlpatterns = [
    path('', views.index, name='index'),
] + auth_urlpatterns
