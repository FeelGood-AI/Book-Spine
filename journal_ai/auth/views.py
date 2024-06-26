import datetime
from journal_ai.auth.models import NotificationSettings, UserData

from journal_ai.prompt_creator.models import Prompt
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from rest_framework.decorators import api_view


class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users info whereas
    a POST request allows to create a new user.
    """

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            fetched_user = User.objects.filter(username=request.data['username']).first() 
            if fetched_user:
                fetched_userData, _ = UserData.objects.get_or_create(user=fetched_user)
                return Response(
                    {
                        'username': fetched_user.username,
                        'id': fetched_user.id,
                        'onboarding_complete': fetched_userData.onboarding_complete,
                    },
                    status=status.HTTP_200_OK
                )
            if serializer.is_valid(raise_exception=ValueError):
                created_user = serializer.create(validated_data=request.data)
                created_user_data = UserData.objects.create(user=created_user)
                now = datetime.datetime.now() - datetime.timedelta(days=2)
                all_prompts = Prompt.objects.filter(date__gte=now.date())
                for prompt in all_prompts:
                    prompt.users.add(created_user)
                    prompt.save()
                
                return Response(
                    {
                        'username': created_user.username,
                        'id': created_user.id,
                        'onboarding_complete': created_user_data.onboarding_complete,
                    },
                    status=status.HTTP_201_CREATED
                )
        except:
            return Response(
                {
                    "error": True,
                    "error_msg": "Server is broken due to request, check what you are sending",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    

@api_view(['POST'])
def acceptOnboardingForUser(request):
    user = User.objects.filter(username=request.data['username']).first()
    if not user:
        return Response({
            'error': 'Invalid User'
        }) 

    user_data = UserData.objects.filter(user=user).first()
    user_data.onboarding_complete = True
    user_data.save()
    return Response({
        'username': user_data.user.username,
        'id': user_data.user.pk,
        'onboarding_complete': user_data.onboarding_complete,
})

@api_view(['POST'])
def setNotificationSettings(request):
    user = User.objects.filter(pk=request.data['user_id']).first()
    if not user:
        return Response({
            'error': 'Invalid User'
        }) 
    # TODO: USE SERIALIZER
    notification_settings = NotificationSettings.objects.filter(user=user).first()
    if notification_settings:
        notification_settings.timezoneName = request.data['timezone_name']
        notification_settings.timezoneOffset = request.data['timezone_offset']
        notification_settings.fcmToken = request.data['fcm_token']
        notification_settings.save()
    else:
        notification_settings = NotificationSettings.objects.create(user=user, timezoneName=request.data['timezone_name'], timezoneOffset=request.data['timezone_offset'],fcmToken=request.data['fcm_token'])
        return Response({
            'user_id': user.pk,
            'timezone_name': notification_settings.timezoneName,
            'timezone_offset': notification_settings.timezoneOffset,
            'fcm_token': notification_settings.fcmToken,
        }, status=status.HTTP_201_CREATED)
    return Response({
        'user_id': user.pk,
        'timezone_name': notification_settings.timezoneName,
        'timezone_offset': notification_settings.timezoneOffset,
        'fcm_token': notification_settings.fcmToken,
    }, status=status.HTTP_200_OK)
