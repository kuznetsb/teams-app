from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(verbose_name="назва", max_length=128, unique=True)
    created_at = models.DateTimeField(
        verbose_name="дата та час створення", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="дата та час оновлення", auto_now=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="автор",
        related_name="created_teams",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "teams"
        verbose_name = "Команда"
        verbose_name_plural = "Команди"


class TeamMember(models.Model):
    team = models.ForeignKey(Team, related_name="members", on_delete=models.CASCADE)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="teams", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        verbose_name="дата та час створення", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="дата та час оновлення", auto_now=True
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="додано користувачем",
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        db_table = "teams_members"
        unique_together = ["team", "member"]
