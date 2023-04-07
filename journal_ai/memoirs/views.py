import datetime
import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MemoirPostSerializer, MemoirSerializer
from rest_framework import status
from .models import Memoir
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
import hashlib
import requests
from ..insights.models import Insight
from .tasks import get_insight
BASE_ENDPOINT = os.environ.get('BASE_ENDPOINT')



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
        # print("post request data:", request.data)
        serializer = MemoirPostSerializer(data=request.data)
        # print("created serializer")
        if serializer.is_valid(raise_exception=ValueError):
            # print("serializer is valid")
            memoir = serializer.create(validated_data=request.data)
            print(request.data['journaler'].id)
            print(memoir.id)
            get_insight.delay(request.data['journaler'].id, memoir.id)
            response_dict = serializer.data
            response_dict['id'] = memoir.id
            print("response dict:", response_dict)
            return Response(
                response_dict,
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
def getMemoirByMemoirId(request, memoir_id):
    memoir = Memoir.objects.filter(pk=memoir_id).first()
    if memoir:
        insight = Insight.objects.filter(memoir=memoir).first()
        if insight:
            serializer = MemoirSerializer(memoir)
            response_dict = serializer.data
            response_dict['insight_available'] = True
            return Response(response_dict)
        else:
            response_dict = {}
            response_dict['insight_available'] = False
            return Response(response_dict)

    return Response({
        'error': 'Invalid memoir id'
    })

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
@api_view(['GET'])
def getMemoirsByDate(request, auth_key):
    test = bytes(auth_key, 'utf-8')
    result = hashlib.md5(test).hexdigest()
    if result != os.getenv('AUTH_KEY'):
        return Response({
            'error': 'Invalid auth key'
        })

    date = request.query_params.get('date', None)
    if date:
        db_date = datetime.date(*[int(x) for x in date.split('-')])
        memoirs = Memoir.objects.filter(prompt__date=db_date)
        serializer = MemoirSerializer(memoirs, many=True)
        return Response(serializer.data)
    return Response({
        'error': 'Invalid Date specified'
    })


@api_view(['GET'])
def getNoInsightMemoirsByDate(request, auth_key):
    test = bytes(auth_key, 'utf-8')
    result = hashlib.md5(test).hexdigest()
    if result != os.getenv('AUTH_KEY'):
        return Response({
            'error': 'Invalid auth key'
        })

    date = request.query_params.get('date', None)
    if date:
        db_date = datetime.date(*[int(x) for x in date.split('-')])
        memoirs = Memoir.objects.filter(prompt__date=db_date, insight=None)
        serializer = MemoirSerializer(memoirs, many=True)
        return Response(serializer.data)
    return Response({
        'error': 'Invalid Date specified'
    })

