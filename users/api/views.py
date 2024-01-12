from datetime import timedelta

from django.conf import settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, status, views
from rest_framework.response import Response

from api.utils import token_login, token_logout

from .serializers.general import UserSerializer, AuthTokenSerializer
from .serializers.input import UserInputSerializer


class CurrentUserView(generics.RetrieveAPIView):
    """Get authenticated user information."""

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class TokenCreateView(ObtainAuthToken):
    """Create API token for given credentials."""

    permission_classes = []
    authentication_classes = []
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context=self.get_serializer_context()
        )
        if serializer.is_valid():
            token = token_login(request, user=serializer.validated_data["user"])
            expired_at = token.created + timedelta(
                seconds=settings.API_TOKEN_EXPIRATION
            )
            return Response({"token": token.key, "expired_at": expired_at})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenDestroyView(views.APIView):
    """Destroy API token for authenticated user and logout existing session."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        token_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateUserView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserInputSerializer
