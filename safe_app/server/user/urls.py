from django.urls import include, path

from server.user import views


urlpatterns = [
    path('', views.index, name='index'),
]
