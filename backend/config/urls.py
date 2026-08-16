"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', views.health, name='health'),
    path('ready/', views.ready, name='ready'),
    path('api/v1/', include([
        path('', include('users.urls')),
        path('', include('courses.urls')),
        path('', include('assessments.urls')),
        path('', include('progress.urls')),
    ])),
]