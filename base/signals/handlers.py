from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.models import OTP, Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])
        OTP.objects.create(user=kwargs["instance"])
        print("user created")
