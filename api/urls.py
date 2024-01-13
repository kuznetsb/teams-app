from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView

from api.views import TeamsSpectacularSwaggerView

app_name = "api"


urlpatterns = [
    path("users/", include("users.api.urls")),
    path("teams/", include("teams.api.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", TeamsSpectacularSwaggerView.as_view(), name="docs"),
]
