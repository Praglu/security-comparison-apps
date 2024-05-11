from django.urls import path

from server.user import auth


urlpatterns = [
    path('login', auth.login_function, name='login'),
    path('logout', auth.logout_function, name='logout'),
]
