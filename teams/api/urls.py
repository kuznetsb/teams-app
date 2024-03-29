from django.urls import path

from teams.api import views

app_name = "teams"

urlpatterns = [
    path("list/", views.TeamViewSet.as_view({"get": "list"}), name="team-list"),
    path("create/", views.TeamViewSet.as_view({"post": "create"}), name="team-create"),
    path(
        "<int:pk>/update/",
        views.TeamViewSet.as_view({"put": "update", "patch": "partial_update"}),
        name="team-update",
    ),
    path(
        "<int:pk>/delete/",
        views.TeamViewSet.as_view({"delete": "destroy"}),
        name="team-delete",
    ),
    path("<int:pk>/detail/", views.TeamDetailView.as_view(), name="team-detail"),
    path(
        "<int:pk>/members-add/",
        views.TeamMembersAddView.as_view(),
        name="team-members-add",
    ),
    path(
        "<int:pk>/members-remove/",
        views.TeamMembersRemoveView.as_view(),
        name="team-members-remove",
    ),
]
