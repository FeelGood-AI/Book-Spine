from django.urls import path
from .views import UserRecordView, acceptOnboardingForUser, setNotificationSettings
from rest_framework.authtoken import views as AuthViews

urlpatterns = [
    path('user/onboarding/', acceptOnboardingForUser, name='user_onboarding'),
    path('user/notification-settings/', setNotificationSettings, name='notifications_settings'),
    path('user/', UserRecordView.as_view(), name='users'),
    path('token/', AuthViews.obtain_auth_token, name='token'),
] 