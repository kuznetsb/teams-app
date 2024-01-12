from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group

from users.models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    ]
    list_display_links = ["email", "first_name", "last_name"]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["id", "email", "first_name", "last_name"]
