from django.contrib import admin
from extras.admin import LibraryInline, MyTaskInline, StoryInline
from .models import User, Profile, Otp, Friend
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

# Register your models here.
class OTPInline(admin.TabularInline):
    model = Otp


class ProfileInline(admin.TabularInline):
    model = Profile
    min_num = 0
    max_num = 10
    readonly_fields = ["thumbnail",]

    def thumbnail(self, instance):
        if instance.avatar.name != "":
            return format_html(f'<img src="{instance.avatar.url}" class="thumbnail" />')
        return ""


@admin.register(User)
class UserdAdmin(BaseUserAdmin):
    list_editable = ("phone",)
    inlines = [OTPInline, StoryInline, ProfileInline, LibraryInline, MyTaskInline]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("phone", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_phone_verified",
                    "is_email_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_display = [
        "email",
        "id",
        "phone",
        "date_joined",
        "is_phone_verified",
        "is_email_verified",
        "is_active",
    ]

    class Media:
        css = {"all": ["styles.css"]}

    # def ottp(self, user):
    #     return user.ottp


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]
    list_display = [
        "user",
        "id",
        "full_name",
        "avatar",
        "educational_level",
        "location",
        "course",
        "updated",
    ]

@admin.register(Friend)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ["user", "id", "user_id"]
