from django.contrib import admin
from django.urls import path, include
from project.views import SettingsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.main.api.urls')),
    path('audit/', include('apps.audit.urls', namespace='audit')),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('', include('apps.main.urls', namespace='main')),
]
