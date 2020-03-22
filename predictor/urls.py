from django.urls import path

from predictor.views import AddData, GetDataset, ClearDatabase, MakePrediction
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prediction/', views.prediction, name='prediction'),
    path('capture/', AddData.as_view(), name='capture'),
    path('getdataset/', GetDataset.as_view(), name='getdataset'),
    path('admintaskclear/', ClearDatabase.as_view(), name='deleteall'),
    path('predict/', MakePrediction.as_view(), name='deleteall'),
]

views.start_up()
