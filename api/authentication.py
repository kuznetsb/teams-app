from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

from .models import get_token_model


class ExpiringTokenAuthentication(TokenAuthentication):
    """ Token authentication with expiration.
    """
    model = get_token_model()

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        if token.created < timezone.now() - timedelta(seconds=settings.API_TOKEN_EXPIRATION):
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)
