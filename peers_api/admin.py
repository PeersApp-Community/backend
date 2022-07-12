from django.contrib import admin

from extras.admin import SpaceTaskInline
from .models import Chat, ChatMsg, Friend, Space, SpaceMsg, Friend


class SpaceMsgInline(admin.TabularInline):
    # autocomplete_fields = ['product']
    model = SpaceMsg
    min_num = 0
    max_num = 10
    extra = 0


class ChatMsgInline(admin.TabularInline):
    model = ChatMsg
    min_num = 0
    max_num = 10
    extra = 1


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["user1", "id", "user2", "pinned", "deleted", "retrieved"]
    inlines = [
        ChatMsgInline,
    ]


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "host", "created", "updated"]
    inlines = [SpaceMsgInline, SpaceTaskInline]


@admin.register(Friend)
class SpaceAdmin(admin.ModelAdmin):
    pass
    # list_display = ["user", "my_friends"]
