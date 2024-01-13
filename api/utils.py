from datetime import timedelta

from django.conf import settings
from django.contrib.auth import login, logout
from django.utils import timezone

from api.models import get_token_model


def token_login(request, user):
    """Get or create API token for given user.
    If token is expired, create new token.
    """
    Token = get_token_model()
    token, created = Token.objects.get_or_create(user=user)
    if not created and token.created < timezone.now() - timedelta(
        seconds=settings.API_TOKEN_EXPIRATION
    ):
        token.delete()
        token = Token.objects.create(user=user)
        token.created = timezone.now()
        token.save()
    login(request, user)
    return token


def token_logout(request):
    """Delete token for authenticated user and logout request."""
    get_token_model().objects.filter(user=request.user).delete()
    logout(request)
