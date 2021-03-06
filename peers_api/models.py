from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class ChatManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get("user")
        lookup1 = Q(user1=user) | Q(user2=user)
        lookup3 = Q(user1=user) & Q(user2=user)
        qs = self.get_queryset().filter(lookup1).exclude(lookup3).distinct()
        return qs


# ==================================================
# ================Models===========================
# ==================================================


class Space(models.Model):
    name = models.CharField(max_length=200)
    host = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="hosted_spaces"
    )
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="spaces", blank=True)
    admins = models.ManyToManyField(User, related_name="isadmin_spaces", blank=True)
    archived = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-pinned", "-updated", "-created"]

    def __str__(self):
        return f"{self.name}"


class SpaceMsg(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="room_msgs")
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    message = models.TextField()
    file = models.FileField(upload_to="spaces/", null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    stared = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    retrieved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-pinned", "-updated", "-created"]

    def __str__(self):
        return f"{self.sender.username}"


class SpaceThread(models.Model):
    thread_message = models.OneToOneField(
        SpaceMsg, on_delete=models.CASCADE, related_name="threads"
    )

    def __str__(self):
        return f"{self.thread_message.message}"


class Reply(models.Model):
    thread = models.ForeignKey(
        SpaceThread, on_delete=models.CASCADE, related_name="replies"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    message = models.TextField()
    file = models.FileField(upload_to="replies/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"


class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user2")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pinned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    retrieved = models.BooleanField(default=False)
    stared = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    objects = ChatManager()

    def __str__(self) -> str:
        return f"{self.user1} to {self.user2}"

    class Meta:
        ordering = ["pinned", "-updated", "-created"]
        unique_together = ["user1", "user2"]


class ChatMsg(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_msgs")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
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
        return f"{self.sender} -- { self.message}"
