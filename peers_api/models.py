from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class FriendChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    receiver = models.ForeignKey(
        Friend, on_delete=models.PROTECT, related_name="receiver"
    )

    body = models.CharField(max_length=255)
    pinned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    retrieved = models.BooleanField(default=False)


class Organisation(models.Model):
    host = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    description = models.TextField()
    participants = models.ManyToManyField(User, related_name="participants", blank=True)


class Topic(models.Model):
    name = models.CharField(max_length=200)


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    organisation = models.ForeignKey(
        Organisation, related_name="rooms", on_delete=models.CASCADE
    )
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name


class RoomChat(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    organisation = models.ForeignKey(
        Organisation, related_name="rooms_msg", on_delete=models.CASCADE
    )
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    retrieved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]


# class Organisation(models.Model):
#     pass
