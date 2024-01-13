from rest_framework import serializers

from teams.models import Team
from users.api.serializers.general import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ["name", "created_by", "created_at", "updated_at"]
        read_only_fields = ["created_by", "created_at", "updated_at"]
