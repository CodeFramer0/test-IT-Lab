from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from todo.models import *


class TaskSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(read_only=True)
    telegram_user = serializers.PrimaryKeyRelatedField(
        queryset=TelegramUser.objects.all(),
        pk_field=HashidSerializerCharField(source_field="todo.TelegramUser.id"),
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        pk_field=HashidSerializerCharField(source_field="todo.Category.id"),
    )
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
