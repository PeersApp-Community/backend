from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from peers_api.models import Space


@receiver(post_save, sender=Space)
def add_host_to_paticipant(sender, **kwargs):
    if kwargs["created"]:
        space = kwargs["instance"]
        print("adding host")
        space.participants.add(kwargs["instance"].host)
        print("host added")
