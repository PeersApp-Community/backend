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

    def __str__(self) -> str:
        return self.email


class Profile(models.Model):

    MALE = "M"
    FEMALE = "F"
    PREFER_NOT_TO_SAY = "P"

    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
        (PREFER_NOT_TO_SAY, "Prefer not to say"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_query_name="")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, default=PREFER_NOT_TO_SAY
    )
    avatar = models.ImageField(null=True, blank=True, default="avatar.svg")
    location = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username


# "id": 1,
# "password": "pbkdf2_sha256$390000$zMchlXYANNQ9Re82eBWkVg$yQVP0mkU1eidGIdTCfpC1YUnJMFoh4d3klLX7tM/zxw=",
# "is_superuser": true,
# "username": "admin",
# "first_name": "",
# "last_name": "",
# "is_staff": true,
# "is_active": true,
# "email": "admin@domain.com",
# "phone": "07015910956",
# "date_joined": "2022-06-20T10:38:20.588375Z",
# "is_phone_verified": false,
# "is_email_verified": false,
# "last_login": "2022-06-21T11:37:29.238857Z",
# "otp": null,
# "groups": [],
# "user_permissions": []
