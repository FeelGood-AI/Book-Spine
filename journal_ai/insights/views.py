import hashlib
import os
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InsightSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from journal_ai.memoirs.models import Memoir



from .models import Insight

class InsightView(APIView):
    """
    API View to create or get a memoir user.
    """
    permission_classes = []

    def post(self, request):
        serializer = InsightSerializer(data=request.data)
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
def getInsightByMemoir(request, memoir_id):
    memoir = Memoir.objects.filter(pk=memoir_id).first()
    if memoir:
        insight = Insight.objects.filter(memoir=memoir).first()
        serializer = InsightSerializer(insight)
        return Response(serializer.data)
    return Response({
        'error': 'Invalid memoir specified'
    })

@api_view(['POST'])
def putInsightIntoMemoir(request, memoir_id, auth_key):
    result = hashlib.md5(b'{auth_key}').hexdigest()
    if result != os.getenv('AUTH_KEY'):
        return Response({
            'error': 'Invalid auth key'
        })
    user = User.objects.filter(pk=request.data['journaler']).first()
    if not user:
        return Response({
            'error': 'Invalid journaler'
        }) 

    memoir = Memoir.objects.filter(pk=memoir_id).first()
    if not memoir:
         return Response({
            'error': 'Invalid memoir id'
        }) 
    insight = Insight(text=request.data['text'],release_timestamp=request.data['release_timestamp'], memoir=memoir, journaler=user)
    insight.save()
    serializer = InsightSerializer(insight)
    return Response(serializer.data, status=201)



class MarkInsightHelpful(APIView):
    """
    API View to get or post an insight as helpful.
    """
    permission_classes = []

    def get(self, request, insight_id, format=None):
        insight = Insight.objects.get(pk=insight_id)
        if insight:
            return Response({
                'insight_id': insight.id,
                'helpful': insight.helpful
            })
        else:
            return Response({
                'error': 'Invalid insight id'
            })

    def post(self, request, insight_id):
        insight = Insight.objects.get(pk=insight_id)
        if insight:
            insight.helpful = request.data['helpful']
            serializer = InsightSerializer(insight)
            insight.save()
            return Response(serializer.data)
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
        
class MarkInsightRead(APIView):
    """
    API View to get or post an insight as read.
    """
    permission_classes = []

    def get(self, request, insight_id, format=None):
        insight = Insight.objects.get(pk=insight_id)
        if insight:
            return Response({
                'insight_id': insight.id,
                'read': insight.read
            })
        else:
            return Response({
                'error': 'Invalid insight id'
            })

    def post(self, request, insight_id):
        insight = Insight.objects.get(pk=insight_id)
        if insight:
            insight.read = request.data['read']
            serializer = InsightSerializer(insight)
            insight.save()
            return Response(serializer.data)
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)