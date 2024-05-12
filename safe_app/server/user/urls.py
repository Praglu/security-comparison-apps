from django.urls import path

from server.user import views


urlpatterns = [
    path('', views.index, name='index'),
    path('user/user-info', views.user_info, name='user-info'),
    path('user/create-user', views.create_user, name='create-user'),
    path('sign-up', views.sign_up, name='sign-up'),
]
