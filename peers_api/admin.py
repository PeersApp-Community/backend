from django.contrib import admin
from .models import RoomChat, Room, Organisation, Topic, FriendChat

# Register your models here.
@admin.register(Organisation)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "host", "created"]


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


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(FriendChat)
class FriendChatAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "updated", "pinned", "retrieved", "deleted"]
