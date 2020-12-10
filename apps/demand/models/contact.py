from django.db import models
from .demand import Demand


class Contact(models.Model):
    demand = models.ForeignKey(
        Demand,
        on_delete=models.CASCADE,
        null=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nome',
        blank=True
    )
    phone = models.CharField(
        max_length=11,
        verbose_name="Contato",
        blank=True
    )

    class Meta:
        db_table = 'demand_contact'
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        ordering = ['-id']

    def __str__(self):
        return self.uf
