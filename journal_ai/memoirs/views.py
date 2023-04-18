import datetime
import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from journal_ai.memoirs.encryption import AESCipher
from .serializers import MemoirPostSerializer, MemoirSerializer
from rest_framework import status
from .models import Memoir
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
import hashlib
import requests
from ..insights.models import Insight
from .tasks import encrypt_memoir, get_insight
from .models import Memoir

BASE_ENDPOINT = os.environ.get('BASE_ENDPOINT')
ENCRYPTER = AESCipher(os.getenv('AES_CIPHER_KEY'))

class MemoirView(APIView):
    """
    API View to create or get a memoir user.
    """
    permission_classes = []

    def post(self, request):
        serializer = MemoirPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            memoir = serializer.create(validated_data=request.data)
            try:
                get_insight.delay(request.data['journaler'].id, memoir.id)
            except Exception as e:
                print("get_insight failed immediately with: ", e)

            try:
                encrypt_memoir.delay(memoir.id)
            except Exception as e:
                print("encrypt_memoir failed immediately with: ", e)

            
            response_dict = serializer.data
            response_dict['id'] = memoir.id
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

        try:
            # decrypt data
            for memoir in serializer.data:
                if memoir['encrypted'] == True:
                    memoir['text'] = ENCRYPTER.decrypt(memoir['text'])
        except:
            return Response({
                'error': 'Error Decrypting data'
            })
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

