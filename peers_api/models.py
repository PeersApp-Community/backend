from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class ChatManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get("user")
        lookup = Q(person1=user) | Q(person2=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


# ==================================================
# ================Models===========================
# ==================================================


class Space(models.Model):
    name = models.CharField(max_length=200)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants")
    archived = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name


class SpaceMsg(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="room_msgs")
    room = models.ForeignKey(Space, on_delete=models.CASCADE)
    message = models.TextField()
    file = models.FileField(upload_to="rooms/", null=True, blank=True)
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
        return self.author.email


class Chat(models.Model):
    person1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name="person1")
    person2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name="person2")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pinned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    retrieved = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    objects = ChatManager()

    def __str__(self) -> str:
        return f"{self.person1} to {self.person2}"

    class Meta:
        ordering = ["-updated", "-created"]
        unique_together = ["person1", "person2"]


class ChatMsg(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_msgs")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to="chats/% Y/% m/% d/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seen = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    stared = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    retrieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} -- { self.message}"


