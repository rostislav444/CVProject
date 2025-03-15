from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.main.api.urls')),
    path('', include('apps.main.urls')),
]
