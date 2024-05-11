from django.urls import path

from server.user import views


urlpatterns = [
    path('', views.index, name='index'),
]
