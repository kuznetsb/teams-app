from django.conf import settings
from django.db import models


class BaseAccessPolicy:
    """
    Base access policy class
    """

    user: settings.AUTH_USER_MODEL

    def __init__(self, user: settings.AUTH_USER_MODEL):
        self.user = user


class ObjectAccessPolicy(BaseAccessPolicy):
    """
    Base class for object-level policies.
    """

    obj: models.Model

    def __init__(self, user: settings.AUTH_USER_MODEL, obj: models.Model):
        super().__init__(user)
        self.obj = obj

    @property
    def can_see_object(self) -> bool:
        """
        Should return True if user can see object.
        """
        raise NotImplementedError()

    @property
    def can_update_object(self) -> bool:
        """
        Should return True if user can update object.
        """
        raise NotImplementedError()

    @property
    def can_delete_object(self) -> bool:
        """
        Should return True if user can delete object.
        """
        raise NotImplementedError()
