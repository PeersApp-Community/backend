from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from peers_api.models import Space


@receiver(post_save, sender=Space)
def add_host_to_paticipant(sender, **kwargs):
    if kwargs["created"]:
        space = kwargs["instance"]
        space1 = Space.objects.get(id=35)
        print("adding host")
        print(space.id)
        print(space.name)
        print(space.participants.all())
        print(space1.participants.all())
        space.participants.add(space.host_id)
        space.save()
        print(kwargs["instance"].participants)
        print(space.participants.all())
        print("host added")
