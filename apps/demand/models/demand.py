from django.db import models
from django.conf import settings


class Demand(models.Model):
    description = models.TextField(
        verbose_name='Descrição',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Anunciante'
    )
    status = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'demand'
        verbose_name = 'Demanda'
        verbose_name_plural = 'Demandas'
        ordering = ['-id']

    def __str__(self):
        return self.description
