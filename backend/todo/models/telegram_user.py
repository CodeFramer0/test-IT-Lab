from django.db import models
from hashid_field import HashidAutoField


class TelegramUser(models.Model):
    id = HashidAutoField(
        primary_key=True,
        salt="telegram_user_salt",
        min_length=10,
        verbose_name="ID",
    )
    name = models.CharField(max_length=50, verbose_name="Имя")
    nick_name = models.CharField(
        max_length=256, default="NoName", verbose_name="Никнейм"
    )
    user_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    class Meta:
        verbose_name = "Telegram пользователь"
        verbose_name_plural = "Telegram пользователи"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.nick_name} ({self.name}) — TG ID: {self.user_id}"
