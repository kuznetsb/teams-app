from typing import Type

from django.conf import settings
from rest_framework.permissions import BasePermission

from api.permissions import ObjectAccessPolicyPermission
from teams_app.services.access_policy import ObjectAccessPolicy


class UserAccessPolicy(ObjectAccessPolicy):
    obj: settings.AUTH_USER_MODEL

    def __init__(self, user: settings.AUTH_USER_MODEL, obj: settings.AUTH_USER_MODEL):
        super().__init__(user, obj)

    @property
    def can_update(self) -> bool:
        """
        If user can update the user page.
        """
        return self.user == self.obj


def user_access_permission(property_name: str) -> Type[BasePermission]:
    """
    Create new permission class, which delegates object permission check to property from UserAccessPolicy.
    """
    permission_class = ObjectAccessPolicyPermission.create_subclass(
        access_policy_class=UserAccessPolicy,
        property_name=property_name,
    )
    return permission_class
