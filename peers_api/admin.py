from django.contrib import admin

from extras.admin import SpaceTaskInline
from .models import Chat, ChatMsg, Space, SpaceMsg


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
    list_display = ["id", "person1", "person2", "pinned", "deleted", "retrieved"]
    inlines = [
        ChatMsgInline,
    ]


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ["name", "host", "created", "updated"]
    inlines = [SpaceMsgInline, SpaceTaskInline]
