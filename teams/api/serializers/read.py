from teams.api.serializers.general import TeamSerializer
from teams.models import Team
from users.api.serializers.general import UserSerializer


class TeamReadSerializer(TeamSerializer):
    members = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Team
        fields = TeamSerializer.Meta.fields + ["members"]
        read_only_fields = fields
