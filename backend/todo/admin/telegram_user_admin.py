from django.contrib import admin
from todo.models import TelegramUser

from .mixins import HashidAdminMixin


@admin.register(TelegramUser)
class TelegramUserAdmin(HashidAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "nick_name", "user_id", "date_joined")
    search_fields = ("name", "nick_name", "user_id")
    ordering = ("-date_joined",)
    readonly_fields = (
        "id",
        "date_joined",
    )
