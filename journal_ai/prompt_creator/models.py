import uuid
from django.db import models
from django.contrib.auth.models import User


PROMPT_TYPES = (
    ("1", "Gratitude"),
    ("2", "Random"),
    ("3", "Anxiety"),
    ("4", "Introspection"),
)
class Prompt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text= models.CharField(max_length=500)
    date = models.DateField()
    users = models.ManyToManyField(User)
    icon = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=25,choices=PROMPT_TYPES, default='2')
