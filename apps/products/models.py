from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import BaseModel


class Product(BaseModel):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='products',
    )
    name = models.CharField(max_length=2048)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']
        db_table = 'products'
