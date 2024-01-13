from django.conf import settings
from django.db import transaction

from teams.models import Team, TeamMember


class TeamManager:
    def __init__(self, team: Team, user: settings.AUTH_USER_MODEL):
        self.team = team
        self.user = user

    @transaction.atomic
    def add_members(self, members: list[settings.AUTH_USER_MODEL]):
        already_added = set(self.team.members.all())
        members_to_add = set(members) - already_added
        new_team_members = [
            TeamMember(team=self.team, member=member, added_by=self.user)
            for member in members_to_add
        ]
        TeamMember.objects.bulk_create(new_team_members)
        return self.team

    def remove_members(self, members: list[settings.AUTH_USER_MODEL]):
        TeamMember.objects.filter(team=self.team, member__in=members).delete()
        return self.team
