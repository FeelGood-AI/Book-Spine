import uuid
from django.db import models
from django.contrib.auth.models import User


PROMPT_TYPES = (
    ("Gratitude", "Gratitude"),
    ("Random", "Random"),
    ("Anxiety", "Anxiety"),
    ("Introspection", "Introspection"),
)
class Prompt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text= models.CharField(max_length=500)
    date = models.DateField()
    users = models.ManyToManyField(User)
    icon = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=25,choices=PROMPT_TYPES, default='Random')
    example_text= models.CharField(max_length=500 , null=True, default="Write Something...")
