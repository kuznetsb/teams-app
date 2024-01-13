from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from teams.api.permissions import IsCreatedByOrAdminOrReadOnly
from teams.api.serializers.general import TeamSerializer
from teams.models import Team


class TeamViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated, IsCreatedByOrAdminOrReadOnly]
    serializer_class = TeamSerializer
    queryset = Team.objects.select_related("created_by")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
