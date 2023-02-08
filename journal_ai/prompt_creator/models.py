from django.db import models
from django.contrib.auth.models import User


class Prompt(models.Model):
    id = models.IntegerField(primary_key=True)
    text= models.CharField(max_length=500)
    date = models.DateField()
    users = models.ManyToManyField(User)
