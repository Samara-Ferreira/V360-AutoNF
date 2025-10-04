from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_rest.urls'), name='api_rest_urls'),  # Include the api_rest app URLs
]
