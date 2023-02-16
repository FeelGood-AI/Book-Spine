from .models import Insight
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class InsightSerializer(serializers.ModelSerializer):
    prompt_text = serializers.ReadOnlyField(source='getPromptText')
    memoirs_text = serializers.ReadOnlyField(source='getMemoirText')

    def create(self, validated_data):
        memoir = Insight.objects.create(**validated_data)
        return memoir

    class Meta:
        model = Insight
        fields = (
            'journaler',
            'helpful',
            'prompt_text',
            'memoirs_text',
            'release_timestamp',
            'read',
            'text',
            'id',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Insight.objects.all(),
                fields=['id','prompt_text', 'memoir_text']
            )
        ]
