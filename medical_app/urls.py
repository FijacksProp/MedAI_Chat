# This file should be in your app directory (medical_app/urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('chat/', views.chat_view, name='chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/initial-consultation/', views.initial_consultation_api, name='initial_consultation'),
]