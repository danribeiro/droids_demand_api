from django.db import models
from .demand import Demand


class Uf(models.Model):
    uf = models.CharField(
        max_length=2,
        unique=True,
        null=False,
        db_column='uf',
        verbose_name="Uf",
    )
    name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        verbose_name="Nome",
    )

    class Meta:
        db_table = 'uf'

    def __str__(self):
        return self.uf


class City(models.Model):
    name = models.CharField(
        max_length=150,
        unique=False,
        null=False,
        verbose_name="Nome",
    )
    uf = models.ForeignKey(
        Uf,
        on_delete=models.PROTECT,
        verbose_name="Uf"
    )

    class Meta:
        db_table = 'city'

    def __str__(self):
        return self.name


class Address(models.Model):
    demand = models.OneToOneField(
        Demand,
        on_delete=models.CASCADE,
        null=True
    )
    street = models.CharField(
        max_length=100,
        verbose_name="Rua",
        blank=True
    )
    number = models.CharField(
        max_length=9,
        verbose_name="Número",
        blank=True
    )
    complement = models.CharField(
        max_length=255,
        verbose_name="Complemento",
        blank=True
    )
    sector = models.CharField(
        max_length=200,
        verbose_name="Bairro",
        blank=True
    )
    zipcode = models.CharField(
        max_length=8,
        verbose_name="CEP",
        blank=True
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Cidade",
    )
    uf = models.ForeignKey(
        Uf,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Uf",
    )

    class Meta:
        db_table = 'demand_address'
        verbose_name = 'Endereço de entrega'
        verbose_name_plural = 'Endereços de entrega'
        ordering = ['-id']

    def __str__(self):
        complete_address = """
        {0}, {1}, {2}\n {3}\n {4}-{5}\n {6}
        """.format(
            self.street,
            self.number,
            self.sector,
            self.complement,
            self.city.__str__(),
            self.uf.__str__(),
            self.zipcode
        )
        return complete_address
