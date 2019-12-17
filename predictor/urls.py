from django.urls import path

from predictor.views import AddData, GetDataset
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('capture/', AddData.as_view(), name='capture'),
    path('getdataset/', GetDataset.as_view(), name='getdataset'),
]