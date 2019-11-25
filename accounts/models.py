from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_male = models.BooleanField(default=False) # 남:True, 여:False User 정보에도!
    image = models.ImageField()
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followings',
        blank=True
    )