from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.fields import PrimaryKeyRelatedOptimizedField


class TeamMembersInputSerializer(serializers.Serializer):
    members = PrimaryKeyRelatedOptimizedField(
        queryset=get_user_model().objects.all(), many=True, required=True
    )

    def validate_members(self, members):
        user = self.context["request"].user
        if not user.is_admin:
            if any(member != user for member in members):
                raise serializers.ValidationError(
                    "Not admin can only add or remove himself to team"
                )
        return members
