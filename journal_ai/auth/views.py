import datetime

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
    permission_classes = [IsAdminUser]

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            fetched_user = User.objects.filter(username=request.data['username']).first()
            if fetched_user:
                return Response(
                    {
                        'username': fetched_user.username,
                        'id': fetched_user.id,
                    },
                    status=status.HTTP_200_OK
                )
            if serializer.is_valid(raise_exception=ValueError):
                created_user = serializer.create(validated_data=request.data)
                now = datetime.datetime.now()
                all_prompts = Prompt.objects.filter(date__gte=now.date())
                for prompt in all_prompts:
                    prompt.users.add(created_user)
                    prompt.save()
                
                return Response(
                    {
                        'username': created_user.username,
                        'id': created_user.id,
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