from rest_framework import serializers
from journal_ai.models import Test

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Test
        fields=('name','id', 'abc')