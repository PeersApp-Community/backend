from django.contrib import admin
from .models import RoomChat, Room, Organisation, Topic, FriendChat, Friend

# Register your models here.
@admin.register(Organisation)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(RoomChat)
class RoomChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Friend)
class FriendChatAdmin(admin.ModelAdmin):
    pass


@admin.register(FriendChat)
class FriendChatAdmin(admin.ModelAdmin):
    pass
