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

@api_view(['GET'])
def getUserByUserName(request, username):
        user = User.objects.filter(username=username).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({
            'error': 'Invalid user specified'
        })