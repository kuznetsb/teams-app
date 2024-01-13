from drf_spectacular.views import SpectacularSwaggerView


class TeamsSpectacularSwaggerView(SpectacularSwaggerView):
    url_name: str = "api:schema"
