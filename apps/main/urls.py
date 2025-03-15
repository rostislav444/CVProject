from django.urls import path
from . import views

urlpatterns = [
    path('', views.CVListView.as_view(), name='cv-list'),
    path('cv/<int:pk>/', views.CVDetailView.as_view(), name='cv-detail'),
]