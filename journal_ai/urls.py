"""journal_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from journal_ai.core import views as core_views

urlpatterns = [
    path("", core_views.index),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("stats/", include('journal_ai.core.urls')),
    path("auth/", include('journal_ai.auth.urls')),
    path("prompt/", include('journal_ai.prompt_creator.urls')),
    path("memoir/", include('journal_ai.memoirs.urls')),
    path("insight/", include('journal_ai.insights.urls'))
]
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

