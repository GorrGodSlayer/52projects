from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_waiter = models.BooleanField(default=False)

class AccessKey(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    @classmethod
    def generate_key(cls, expiration_days=30):
        expires_at = timezone.now() + timezone.timedelta(days=expiration_days)
        return cls.objects.create(expires_at=expires_at)

    def is_valid(self):
        return self.is_active and self.expires_at > timezone.now()
