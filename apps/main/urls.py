from django.urls import path
from apps.main import views

app_name = 'main'

urlpatterns = [
    # Web views
    path('', views.CVListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', views.CVDetailView.as_view(), name='cv_detail'),
    path('cv/<int:pk>/pdf/', views.CVPDFView.as_view(), name='cv_pdf'),
    path('cv/<int:pk>/email-pdf/', views.CVEmailPDFView.as_view(), name='cv_email_pdf'),
]