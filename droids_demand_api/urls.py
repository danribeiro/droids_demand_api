import rest_framework
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from apps.demand.views import *
from apps.accounts.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token, name="auth"),
    path('api-token-verify/', verify_jwt_token, name="verify"),

    path('user/', UserView.as_view(), name='user_create'),
    path('ufs/', UfListView.as_view(), name='uf_list'),
    path('uf/<int:uf>/cities/', CityListView.as_view(), name='city_list'),
    path('demand/', DemandCreateView.as_view(), name='demand_create'),
    path('demand/<int:pk>', DemandUpdateDeleteView.as_view(),
         name='demand_update_delete'),
    path('demands/', DemandListView.as_view(), name='demand_list'),
    path('demand/<int:pk>/status/update/',
         DemandStatusUpdateView.as_view(), name='demand_status_update'),
]
