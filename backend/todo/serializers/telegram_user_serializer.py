from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from todo.models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(source_field=TelegramUser.id, read_only=True)

    class Meta:
        model = TelegramUser
        fields = "__all__"
