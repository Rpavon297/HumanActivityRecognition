from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('capture/', views.update_data, name='capture'),
]