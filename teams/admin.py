from django.contrib import admin

from teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created_at",
        "updated_at",
        "created_by",
    ]
    list_display_links = ["name"]
    list_filter = ["created_by"]
    search_fields = ["name"]
