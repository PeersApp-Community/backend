import datetime
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from datetime import datetime

User = settings.AUTH_USER_MODEL


class Organisation(models.Model):
    host = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name="members", blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=200)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    organisation = models.ForeignKey(
        Organisation, related_name="rooms", on_delete=models.CASCADE
    )
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
    seen = models.BooleanField(default=False)
    stared = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    retrieved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]


class Status(models.Model):
    user = models.OneToOneField(
        User, verbose_name=_("status"), on_delete=models.CASCADE
    )
    post = models.FileField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)


class FriendChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="receiver"
    )
    body = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    stared = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    retrieved = models.BooleanField(default=False)

    def __str__(self):
        return self.sender


#
#
#
# class Stared(models.Model):
#     user = models.OneToOneField(
#         User, verbose_name=_("Users stared messages"), on_delete=models.CASCADE
#     )
#     stared_room_msg = models.ForeignKey(
#         RoomChat, verbose_name=_("Stared Room Messages"), on_delete=models.CASCADE
#     )
#     stared_friend_msg = models.ForeignKey(
#         FriendChat, verbose_name=_("Stared Friends Messages"), on_delete=models.CASCADE
#     )


# class Topic(models.Model):
#     title = models.CharField(max_length=200)
#     organisation = models.ForeignKey(
#         Organisation, on_delete=models.CASCADE, related_name="topics"
#     )

#     def __str__(self):
#         return self.title

# class Friend(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
