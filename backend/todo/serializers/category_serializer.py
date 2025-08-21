from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from todo.models import Category


class CategorySerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(source_field=Category.id, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
