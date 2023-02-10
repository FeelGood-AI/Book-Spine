from django.db import models
from django.contrib.auth.models import User

from journal_ai.prompt_creator.models import Prompt


class Memoir(models.Model):
    id = models.IntegerField(primary_key=True)
    text= models.CharField(max_length=5000)
    journaler = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    prompt = models.ForeignKey(Prompt,null=True, on_delete=models.SET_NULL)

    def getPromptText(self):
        return self.prompt.text if self.prompt else ''
