from django.urls import path

from server.transfer import views


urlpatterns = [
    path('create-transfer', views.create_transfer, name='create-transfer'),
    path('post-transfer', views.post_transfer, name='post-transfer'),
]
