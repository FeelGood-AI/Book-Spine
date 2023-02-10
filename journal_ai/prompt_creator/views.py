from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PromptSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import datetime



from journal_ai.prompt_creator.models import Prompt

class PromptView(APIView):
    """
    API View to create or get a list of prompts
    """
    permission_classes = []

    def get(self, request, pk, format=None):
        prompt = Prompt.objects.get(pk=pk)
        serializer = PromptSerializer(prompt)
        return Response(serializer.data)

    def post(self, request):
        serializer = PromptSerializer(data=request.data)
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
def getPromptsByDate(request, user_id):
    date = request.query_params.get('date', None)
    if date:
        db_date = datetime.date(*[int(x) for x in date.split('-')])
        prompts = Prompt.objects.filter(date=db_date, users__in=[user_id])
        serializer = PromptSerializer(prompts, many=True)
        return Response(serializer.data)
    return Response({
        'error': 'Invalid Date specified'
    })
