from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.models import Otp, Profile, Friend


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        user = kwargs["instance"]
        Profile.objects.create(user=user, id=user.id)
        Otp.objects.create(user_id=user.id, id=user.id)
        Friend.objects.create(user_id=user.id, id=user.id)
        print("user created")
