from journal_ai.prompt_creator.serializers import PromptSerializer
from .models import Memoir
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class MemoirSerializer(serializers.ModelSerializer):
    prompt_text = serializers.ReadOnlyField(source='getPromptText')

    def create(self, validated_data):
        memoir = Memoir.objects.create(**validated_data)
        return memoir

    class Meta:
        model = Memoir
        fields = (
            'journaler',
            'timestamp',
            'prompt_text',
            'text',
            'id',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Memoir.objects.all(),
                fields=['journaler','timestamp', 'prompt']
            )
        ]