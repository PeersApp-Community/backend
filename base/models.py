from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    otp = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "email"]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_query_name="")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, default="avatar.svg")
    updated = models.DateTimeField(auto_now=True)
