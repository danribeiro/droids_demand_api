from django.urls import path, include
from .views import *


urlpatterns = [
    path('', DemandCreateView.as_view(), name='demand_create'),
    path('ufs/', UfListView.as_view(), name='uf_list'),
    path('uf/<int:uf>/cities/', CityListView.as_view(), name='city_list'),
]
