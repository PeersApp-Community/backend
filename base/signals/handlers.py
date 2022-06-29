from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.models import Otp, Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])
        # Otp.objects.create(user_id=kwargs["instance"].id)
        print("user created")
