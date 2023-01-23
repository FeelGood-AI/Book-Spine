from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=80)
    id = models.IntegerField(primary_key=True)
    abc= models.CharField(max_length=100)