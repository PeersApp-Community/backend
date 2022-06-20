from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
@admin.register(User)
class UserdAdmin(BaseUserAdmin):
    list_editable = ("otp","phone")
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
                    "otp",
                ),
            },
        ),
    )

    list_display = [
        "id",
        "email",
        "phone",
        "otp",
        "date_joined",
        "is_phone_verified",
        "is_email_verified",
        "is_active"
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]
    list_display = ["user_id", "id", "user", "first_name", "last_name", "avatar"]
