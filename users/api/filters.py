from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters


class UserFilterSet(filters.FilterSet):
    is_admin = filters.BooleanFilter(field_name="is_superuser")
    first_name = filters.CharFilter(lookup_expr="icontains")
    last_name = filters.CharFilter(lookup_expr="icontains")
    email = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = get_user_model()
        fields = []
