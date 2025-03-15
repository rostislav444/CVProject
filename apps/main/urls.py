from django.urls import path
from apps.main import views

app_name = 'main'

urlpatterns = [
    # Web views
    path('', views.CVListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', views.CVDetailView.as_view(), name='cv_detail'),
]