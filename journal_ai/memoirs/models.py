import uuid
from django.db import models
from django.contrib.auth.models import User

from journal_ai.prompt_creator.models import Prompt


class Memoir(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text= models.CharField(max_length=5000)
    journaler = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    prompt = models.ForeignKey(Prompt,null=True, on_delete=models.SET_NULL)

    def getPrompt(self):
        if self.prompt:
            return {
                'text': self.prompt.text,
                'date': self.prompt.date
            }
        return {}

    def getInsight(self):
        insight = self.insight_set.all().first()
        if insight:
            return {
                'text': insight.text,
                'helpful': insight.helpful,
                'read': insight.read,
                'id': insight.id,
            }
        return {}
