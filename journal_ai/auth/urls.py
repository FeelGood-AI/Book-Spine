from django.urls import path
from .views import UserRecordView, acceptOnboardingForUser
from rest_framework.authtoken import views as AuthViews

urlpatterns = [
    path('user/onboarding/', acceptOnboardingForUser, name='user_onboarding'),
    path('user/', UserRecordView.as_view(), name='users'),
    path('token/', AuthViews.obtain_auth_token, name='token'),
] 