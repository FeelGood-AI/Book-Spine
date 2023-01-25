from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('view', views.getTest),
    path('add/', views.postTest),
]