from django.urls import path

from server.user import views


urlpatterns = [
    path('', views.index, name='index'),
    path('user/user-info', views.user_info, name='user-info'),
]
