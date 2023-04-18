from journal_ai.prompt_creator.models import Prompt
from .models import Memoir
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User



class MemoirSerializer(serializers.ModelSerializer):
    prompt = serializers.ReadOnlyField(source='getPrompt')
    insight = serializers.ReadOnlyField(source='getInsight')

    def create(self, validated_data):
        memoir = Memoir.objects.create(**validated_data)
        return memoir

    class Meta:
        model = Memoir
        fields = (
            'journaler',
            'timestamp',
            'prompt',
            'text',
            'id',
            'insight',
            'encrypted'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Memoir.objects.all(),
                fields=['journaler','timestamp', 'prompt']
            )
        ]

class MemoirPostSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        journaler = User.objects.filter(pk=validated_data['journaler']).first()
        prompt = Prompt.objects.filter(pk=validated_data['prompt']).first()
        validated_data['journaler'] = journaler
        validated_data['prompt'] = prompt
        try:
            memoir = Memoir.objects.create(**validated_data)
        except:
            return {
                'error': "Invalid journaler or prompt",
            } 
        return memoir

    class Meta:
        model = Memoir
        fields = (
            'journaler',
            'timestamp',
            'prompt',
            'text',
            'id',
            'encrypted'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Memoir.objects.all(),
                fields=['journaler','timestamp', 'prompt']
            )
        ]