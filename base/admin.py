from django.contrib import admin
from peers_api.admin import StoryInline
from .models import User, Profile, Otp
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


# Register your models here.
class OTPInline(admin.TabularInline):
    model = Otp


@admin.register(User)
class UserdAdmin(BaseUserAdmin):
    list_editable = ("phone", )
    inlines = [OTPInline, StoryInline]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone", "email")}),
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
        "id",
        "email",
        "phone",
        "date_joined",
        "is_phone_verified",
        "is_email_verified",
        "is_active",
    ]
    
    # def ottp(self, user):
    #     return user.ottp


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]
    list_display = ["user_id", "id", "user", "first_name", "last_name", "avatar"]
