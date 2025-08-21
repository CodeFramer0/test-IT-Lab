import django_filters
from todo.models import TelegramUser


class TelegramUserFilter(django_filters.FilterSet):
    user_id = django_filters.CharFilter(field_name="user_id", lookup_expr="exact")

    class Meta:
        model = TelegramUser
        fields = ["user_id"]
