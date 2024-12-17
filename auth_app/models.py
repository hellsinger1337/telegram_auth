from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta

class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150)

class LoginToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE,null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)