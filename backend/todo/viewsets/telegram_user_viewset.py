from rest_framework import viewsets
from todo.filters import TelegramUserFilter
from todo.models import TelegramUser
from todo.serializers.telegram_user_serializer import TelegramUserSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    filterset_class = TelegramUserFilter
