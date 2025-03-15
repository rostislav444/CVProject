from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.main.api.urls')),
    path('audit/', include('apps.audit.urls', namespace='audit')),
    path('', include('apps.main.urls', namespace='main')),
]
