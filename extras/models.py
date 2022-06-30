from django.db import models
from django.conf import settings
from peers_api.models import Space

# Create your models here.

User = settings.AUTH_USER_MODEL


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="story")
    file = models.FileField(upload_to="status", null=True, blank=True)
    text = models.CharField(max_length=50, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        ordering = ["-updated", "-created"]


class Library(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="library",
    )
    file = models.FileField(upload_to="status", null=True, blank=True)
    link = models.URLField()


class SpaceTask(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class MyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mytasks")
    title = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
