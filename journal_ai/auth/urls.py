from django.urls import path
from .views import UserRecordView
from rest_framework.authtoken import views as AuthViews

urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('user/', UserRecordView.as_view(), name='users'),

    path('token/', AuthViews.obtain_auth_token, name='token'),
] 