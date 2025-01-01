from django.utils import timezone
from django.db import models

from django.contrib.auth.models import User
from django.utils.timezone import now

import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LoginRecord(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Login de {self.user.username} em {self.login_time}"

    class Meta:
        ordering = ['-created_at']


class LoginAttempt(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="login_attempt")
    last_attempt = models.DateTimeField(auto_now=True)
    attempts = models.PositiveIntegerField(default=0)
    blocked_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
