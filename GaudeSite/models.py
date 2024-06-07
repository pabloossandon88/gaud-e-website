from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)
    profile_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Credits: {self.credits}"
