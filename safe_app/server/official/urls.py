from django.urls import path

from server.official import views


urlpatterns = [
    path('create-official', views.create_official, name='create-official'),
    path('post-official', views.post_official, name='post-official'),
]
