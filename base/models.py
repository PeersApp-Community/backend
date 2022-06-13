from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email" or "phone"
    REQUIRED_FIELDS = ["username", "phone"]


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, default="avatar.svg")
