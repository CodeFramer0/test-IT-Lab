from django.db import models
from hashid_field import HashidAutoField


class Category(models.Model):
    id = HashidAutoField(
        primary_key=True,
        salt="category_salt",
        min_length=8,
        verbose_name="ID",
    )
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name
