from django.contrib import admin
from .models import Chat, ChatMsg, Space, SpaceMsg, Status


class SpaceMsgInline(admin.TabularInline):
    model = SpaceMsg
    # autocomplete_fields = ['product']
    min_num = 0
    max_num = 10
    extra = 0


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ["name", "host", "created", "updated"]
    inlines = [SpaceMsgInline]


class StatusInline(admin.TabularInline):
    model = Status
    min_num = 0
    max_num = 10


class ChatMsgInline(admin.TabularInline):
    model = ChatMsg
    min_num = 0
    max_num = 10
    extra = 1


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id", "person1", "person2", "pinned", "deleted", "retrieved"]
    inlines = [ChatMsgInline]
