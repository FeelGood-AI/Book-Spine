from django.db import models
from django.contrib.auth.models import User
from journal_ai.memoirs.models import Memoir

class Insight(models.Model):
    id = models.IntegerField(primary_key=True)
    text= models.CharField(max_length=2000)
    journaler = models.ForeignKey(User, on_delete=models.CASCADE)
    release_timestamp = models.DateTimeField()
    memoir = models.ForeignKey(Memoir, on_delete=models.CASCADE)
    helpful = models.BooleanField(null=True)
