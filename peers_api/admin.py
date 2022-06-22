from django.contrib import admin
from .models import RoomChat, Room, Organisation, FriendChat, Status
from django.db import models

# Register your models here.
@admin.register(Organisation)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "host", "created"]
    formfield_overrides = {
        models.DateTimeField: {"input_formats": ("%d/%m/%Y",)},
    }


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "host", "organisation", "created", "updated"]


@admin.register(RoomChat)
class RoomChatAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "room",
        "organisation",
        "updated",
        "pinned",
        "retrieved",
        "deleted",
    ]
    formfield_overrides = {
        models.DateTimeField: {"input_formats": ("%d/%m/%Y",)},
    }


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created", "updated"]


@admin.register(FriendChat)
class FriendChatAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "updated", "pinned", "retrieved", "deleted"]
