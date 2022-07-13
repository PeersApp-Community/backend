from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from peers_api.models import SpaceMsg, SpaceThread


@receiver(post_save, sender=SpaceMsg)
def add_host_to_paticipant(sender, **kwargs):
    if kwargs["created"]:
        msg = kwargs["instance"]
        SpaceThread.objects.create(thread_message_id=msg.id, id=msg.id)
        print("Thread Created")
