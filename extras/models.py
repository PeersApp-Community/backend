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
        return f"{self.user.username}"

    class Meta:
        ordering = ["-updated", "-created"]


# class Genre(models.Model):
#     title = models.CharField(max_length=200)
#     created = models.DateField(auto_now_add=True)


class Book(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    author = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="books", null=True, blank=True)
    cover = models.ImageField(upload_to="cover", null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    saved = models.ManyToManyField(User, blank=True, related_name="saved_books")
    public = models.BooleanField(default=False)
    read = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["-updated", "-created"]


class Library(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="lib",
    )
    books = models.ManyToManyField(Book, blank=True, related_name="lib")

    def __str__(self):
        return f"{self.user.username} library"


# PRIORITY_CHOICES PRIORITY_CHOICES PRIORITY_CHOICES
# PRIORITY_CHOICES PRIORITY_CHOICES PRIORITY_CHOICES
HIGH = "H"
MEDIUM = "M"
LOW = "L"

PRIORITY_CHOICES = [
    (HIGH, "HIGH"),
    (MEDIUM, "MEDIUM"),
    (LOW, "LOW"),
]


class SpaceTask(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="tasks")
    task = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default=MEDIUM)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return f"{self.title}"


class MyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    task = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default=MEDIUM)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return f"{self.title}"
