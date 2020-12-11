from django.contrib import admin
from django.urls import path, include
import rest_framework
from rest_framework_jwt.views import obtain_jwt_token
from apps.demand import urls as demand_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_jwt_token),
    path('demand/', include(demand_urls))
]
