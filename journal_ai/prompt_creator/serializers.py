from .models import Prompt
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class PromptSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        prompt = Prompt.objects.create(**validated_data)
        return prompt

    class Meta:
        model = Prompt
        fields = (
            'id',
            'text',
            'date',
            'icon',
            'type',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Prompt.objects.all(),
                fields=['id','date', 'text']
            )
        ]