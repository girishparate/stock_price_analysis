from os import name
from django.urls import path
from .views import *

urlpatterns = [
    path('', Dashboard.as_view(), name='home'),

    path('graph', GraphStock.as_view(), name='graph')
]