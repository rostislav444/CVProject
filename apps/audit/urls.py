from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    path('logs/', views.RecentRequestsView.as_view(), name='recent_requests'),
]