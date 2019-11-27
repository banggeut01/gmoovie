from django.db import models
from accounts.models import User
# Create your models here.
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(blank=True, null=True, max_length=225)
    status = models.CharField(blank=True, null=True, max_length=225)
    created_at = models.DateTimeField(auto_now=True)