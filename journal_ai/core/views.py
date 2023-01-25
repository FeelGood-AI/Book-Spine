from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from journal_ai.models import Test
from journal_ai.core.serializers import TestSerializer

def index(request):
    return render(
        request,
        "index.html",
        {
            "title": "Django example",
        },
    )


# TEST VIEW meant to illustrate how get view are written 
@api_view(['GET'])
def getTest(request):
    food = Test.objects.all()
    serializer = TestSerializer(food, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def postTest(request):
    serializer = TestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)