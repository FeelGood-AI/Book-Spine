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
        insight = Memoir.objects.filter(memoir=memoir).first()
        serializer = InsightSerializer(insight)
        return Response(serializer.data)
    return Response({
        'error': 'Invalid memoir specified'
    })

@api_view(['GET'])
def getInsightByMemoir(request, memoir_id):
    memoir = Memoir.objects.filter(pk=memoir_id).first()
    if memoir:
        insight = Memoir.objects.filter(memoir=memoir).first()
        serializer = InsightSerializer(insight)
        return Response(serializer.data)
    return Response({
        'error': 'Invalid memoir specified'
    })


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
            serializer = InsightSerializer(insight, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        