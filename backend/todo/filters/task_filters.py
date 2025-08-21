import django_filters
from todo.models import Task


class TaskFilter(django_filters.FilterSet):
    is_completed = django_filters.BooleanFilter(field_name="is_completed")
    is_expired = django_filters.BooleanFilter(field_name="is_expired")
    category = django_filters.CharFilter(field_name="category__id", lookup_expr="exact")
    telegram_user = django_filters.CharFilter(
        field_name="telegram_user__id", lookup_expr="exact"
    )

    class Meta:
        model = Task
        fields = ["is_completed", "is_expired", "category", "telegram_user"]
