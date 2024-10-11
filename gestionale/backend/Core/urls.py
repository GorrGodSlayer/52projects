from django.urls import path
from . import views

urlpatterns = [
    path('generate-key/', views.generate_key, name='generate_key'),
    path('validate-key/', views.validate_key, name='validate_key'),
]
