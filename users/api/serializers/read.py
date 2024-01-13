from django.contrib.auth import get_user_model

from teams.api.serializers.general import TeamSerializer
from users.api.serializers.general import UserSerializer


class UserDetailSerializer(UserSerializer):
    teams = TeamSerializer(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = UserSerializer.Meta.fields + ["teams"]
        read_only_fields = fields
