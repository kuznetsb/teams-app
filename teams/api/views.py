from drf_spectacular.utils import extend_schema
from rest_framework import mixins, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from teams.api.permissions import IsCreatedByOrAdminOrReadOnly
from teams.api.serializers.general import TeamSerializer
from teams.api.serializers.input import TeamMembersInputSerializer
from teams.api.serializers.read import TeamReadSerializer
from teams.models import Team
from teams.services.general import TeamManager


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


class TeamDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamReadSerializer

    def get_queryset(self):
        return Team.objects.select_related("created_by").prefetch_related("members")


class TeamManageMixin:
    permission_classes = [IsAuthenticated]
    serializer_class = TeamMembersInputSerializer
    queryset = Team.objects.select_related("created_by").prefetch_related("members")
    team_manager = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["team"] = self.get_object()
        return context

    @extend_schema(responses=TeamReadSerializer)
    def post(self, request, *args, **kwargs):
        team = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={"request": request, "team": team}
        )
        serializer.is_valid(raise_exception=True)
        self.team_manager = TeamManager(team, request.user)
        self.process_objects(serializer.validated_data.get("members"))
        response_serializer = TeamReadSerializer(self.get_object())
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def process_objects(self, objects):
        raise NotImplementedError


class TeamMembersAddView(TeamManageMixin, generics.GenericAPIView):
    def process_objects(self, objects):
        return self.team_manager.add_members(objects)


class TeamMembersRemoveView(TeamManageMixin, generics.GenericAPIView):
    def process_objects(self, objects):
        return self.team_manager.remove_members(objects)
