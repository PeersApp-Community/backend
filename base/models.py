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

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self) -> str:
        return f"{self.id}___{self.username}"

    # def ottp(self):
    #     return self.otp.otp_num


class Otp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp")
    otp_num = models.CharField(max_length=6, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)

    def expiry(self):
        expiry_date = self.created
        return expiry_date

    def __str__(self):
        return str(self.otp_num)


class Profile(models.Model):

    MALE = "M"
    FEMALE = "F"
    PREFER_NOT_TO_SAY = None

    GENDER_CHOICES = [
        (PREFER_NOT_TO_SAY, "Prefer not to say"),
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        null=True,
        blank=True,
        max_length=6,
        choices=GENDER_CHOICES,
        default=PREFER_NOT_TO_SAY,
    )
    avatar = models.ImageField(null=True, blank=True, upload_to="imgs")
    institution = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    educational_level = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    course = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    location = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.full_name}"


class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="friends")
    friend_list = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.user}"
