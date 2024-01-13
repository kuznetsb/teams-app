from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers


class UserInputSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "first_name", "last_name", "is_admin")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate_is_admin(self, value):
        if value and self.instance:
            raise serializers.ValidationError("You can update this only in admin panel")
        return value

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        is_admin = validated_data.pop("is_admin")
        if is_admin:
            return get_user_model().objects.create_superuser(**validated_data)
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
