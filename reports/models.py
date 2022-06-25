from django.conf import settings
from django.db import models


# Create your models here.
class Rating(models.Model):

    RATE_CHOICES = [
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
        (4, "Four"),
        (5, "Five"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(choices=RATE_CHOICES)
