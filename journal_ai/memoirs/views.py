from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MemoirPostSerializer, MemoirSerializer
from rest_framework import status
from .models import Memoir
from rest_framework.decorators import api_view
from django.contrib.auth.models import User



from .models import Memoir

class MemoirView(APIView):
    """
    API View to create or get a memoir user.
    """
    permission_classes = []

    # def get(self, request, format=None):
    #     memoir = Memoir.objects.all()
    #     serializer = MemoirSerializer(memoir, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        serializer = MemoirPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def getMemoirsByUser(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        memoirs = Memoir.objects.filter(journaler=user)
        serializer = MemoirSerializer(memoirs, many=True)
        return Response(serializer.data)
    return Response({
        'error': 'Invalid User specified'
    })
