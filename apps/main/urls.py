from django.urls import path
from apps.main import views



urlpatterns = [
    # Web views
    path('', views.CVListView.as_view(), name='cv-list'),
    path('cv/<int:pk>/', views.CVDetailView.as_view(), name='cv-detail'),
]