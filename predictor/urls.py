from django.urls import path

from predictor.views import AddData, GetDataset, ClearDatabase, MakePrediction, PlotData
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('current/', views.current, name='current'),
    path('capture/', AddData.as_view(), name='capture'),
    path('getdataset/', GetDataset.as_view(), name='getdataset'),
    path('admintaskclear/', ClearDatabase.as_view(), name='deleteall'),
    path('admintaskdiagnostic/', views.invalids, name='check'),
    path('predict/', MakePrediction.as_view(), name='predict'),
    path('plot/', PlotData.as_view(), name='plotdata'),
]

views.start_up()
