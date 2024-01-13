from django.utils.functional import cached_property
from rest_framework import serializers


class PrimaryKeyRelatedOptimizedField(serializers.PrimaryKeyRelatedField):
    @cached_property
    def prefetched_qs(self):
        return {item.pk: item for item in self.get_queryset()}

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        try:
            if isinstance(data, bool):
                raise TypeError
            if self.prefetched_qs and not isinstance(
                data, type(list(self.prefetched_qs.keys())[0])
            ):
                raise TypeError
            return self.prefetched_qs[data]
        except KeyError:
            self.fail("does_not_exist", pk_value=data)
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)
