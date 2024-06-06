from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0) 

    def __str__(self):
        return f"{self.user.username} - Credits: {self.credits}"
