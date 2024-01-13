from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.serializers import (
    AuthTokenSerializer as BaseAuthTokenSerializer,
)

from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
        ]
        read_only_fields = fields


class AuthTokenSerializer(BaseAuthTokenSerializer):
    """Authenticate user by email and password.
    Consider session `auth_error` key, which can be set by auth backends.
    """

    email = serializers.EmailField(label=_("Email"), write_only=True)
    username = None

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context["request"]

        if email and password:
            user = authenticate(request=request, email=email, password=password)

            if not user:
                msg = (
                    request.session.pop("auth_error", None)
                    or "Не вдалось увійти із вказаними даними входу."
                )
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = "Пароль і e-mail обов'язкові."
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
