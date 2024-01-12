from typing import Type

from rest_framework.fields import get_attribute
from rest_framework.permissions import IsAuthenticated, BasePermission

from teams_app.services.access_policy import ObjectAccessPolicy


class AccessPolicyBasePermission(IsAuthenticated):
    base_access_policy_class: type[ObjectAccessPolicy] = None
    access_policy_class: type[ObjectAccessPolicy] = None
    property_name: str = None

    @classmethod
    def create_subclass(
        cls, access_policy_class: ObjectAccessPolicy, property_name: str, **extra_fields
    ) -> Type[BasePermission]:
        # Create subclass with given properties
        class AccessPolicyPermission(cls):
            pass

        # Set provided attributes
        AccessPolicyPermission.access_policy_class = access_policy_class
        AccessPolicyPermission.property_name = property_name
        for field, value in extra_fields.items():
            setattr(AccessPolicyPermission, field, value)

        # Check if provided attributes are valid
        AccessPolicyPermission._check_access_policy_class()
        AccessPolicyPermission._check_property_name()
        AccessPolicyPermission._check_extra_fields()

        return AccessPolicyPermission

    @classmethod
    def _check_access_policy_class(cls):
        """
        Check if ``access_policy_class`` is valid class.
        """
        assert cls.access_policy_class, "``access_policy_class`` must be set."
        assert issubclass(
            cls.access_policy_class, cls.base_access_policy_class
        ), "Provided ``access_policy_class`` must be sublass of the ``{}``.".format(
            cls.base_access_policy_class
        )

    @classmethod
    def _check_property_name(cls):
        """
        Check if property exists in provided ``access_policy_class``.
        """
        assert cls.property_name, "``property_name`` must be set."
        assert isinstance(
            getattr(cls.access_policy_class, cls.property_name, None), property
        ), "Provided ``property_name``({}) must be property of the ``{}``.".format(
            cls.property_name, cls.access_policy_class
        )

    @classmethod
    def _check_extra_fields(cls):
        pass


class ObjectAccessPolicyPermission(AccessPolicyBasePermission):
    """
    Base class for API permissions, where object permission should be
    delegated to ``ObjectAccessPolicy`` subclass.
    """

    base_access_policy_class = ObjectAccessPolicy

    # TODO: delete
    obj_attribute: str | None = None
    view_attribute: str | None = None

    access_policy_object_source: str | None

    def has_object_permission(self, request, view, obj):
        if not super().has_object_permission(request, view, obj):
            return False

        source_dict = {"view": view, "obj": obj}

        if self.access_policy_object_source:
            obj = get_attribute(
                source_dict, self.access_policy_object_source.split(".")
            )
        else:
            if self.view_attribute:
                obj = get_attribute(view, self.view_attribute.split("."))

            if self.obj_attribute:
                obj = get_attribute(obj, self.obj_attribute.split("."))

        if not obj:
            raise Exception(
                f"object for {self.access_policy_class.__name__} is not defined. Permission class - {self.__class__.__name__}."
            )

        object_policy = self.access_policy_class(user=request.user, obj=obj)
        return getattr(object_policy, self.property_name)

    @classmethod
    def create_subclass(
        cls,
        *args,
        obj_attribute: str | None = None,  # old
        view_attribute: str | None = None,  # old
        access_policy_object_source: str | None = None,
        **kwargs,
    ) -> Type[BasePermission]:
        """
        Arguments:
            access_policy_object_source: path where object for AccessPolicy should be taken.
                Examples:
                - 'obj' (take `obj` passed to permission check)
                - 'obj.ticket' (take ticket from `obj` passed to permission check)
                - 'view.object' (take object from view)
                - 'view.custom_attr.sub_attr'

        """
        return super().create_subclass(
            *args,
            obj_attribute=obj_attribute,
            view_attribute=view_attribute,
            access_policy_object_source=access_policy_object_source,
            **kwargs,
        )
