from rest_framework.authtoken.models import Token


def get_token_model():
    """Return model used for token authentication."""
    return Token
