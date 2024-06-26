from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    onboarding_complete = models.BooleanField(default=False)

    def getUser(self):
        return self.user if self.user else ''
    


class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezoneOffset = models.CharField(max_length=100)
    timezoneName = models.CharField(max_length=100)
    fcmToken = models.CharField(max_length=512)


    def getUser(self):
        return self.user if self.user else ''