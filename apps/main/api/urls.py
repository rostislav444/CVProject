from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.main.api import views

# Create a router for the API
router = DefaultRouter()
router.register(r'cvs', views.CVViewSet)
router.register(r'skills', views.SkillViewSet)

# Define the API URL patterns
urlpatterns = [
    path('', include(router.urls)),
]

