import uuid
from django.db import models
from django.contrib.auth.models import User
from journal_ai.memoirs.models import Memoir

class Insight(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text= models.CharField(max_length=2000)
    journaler = models.ForeignKey(User, on_delete=models.CASCADE)
    release_timestamp = models.DateTimeField()
    memoir = models.ForeignKey(Memoir, on_delete=models.CASCADE)
    helpful = models.BooleanField(null=True)

    def getMemoirText(self):
        return self.memoir.text if self.memoir else ''
    
    def getPromptText(self):
        return self.memoir.prompt.text if self.memoir and self.memoir.prompt else ''
