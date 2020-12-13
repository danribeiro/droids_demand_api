import os
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, ContentType)
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager

CHOICES = (
    (1, 'Administrador'),
    (2, 'Anunciante')
)


class User(AbstractBaseUser, PermissionsMixin):
    profile = models.IntegerField(
        verbose_name='Perfil',
        help_text='Tipo de usuário',
        choices=CHOICES,
        default=2
    )
    email = models.EmailField(
        verbose_name='E-mail',
        unique=True,
        max_length=255,
        help_text='Email do usuário'
    )
    first_name = models.CharField(
        verbose_name='Nome',
        max_length=80,
        blank=True,
        help_text='Nome do usuário'
    )
    last_name = models.CharField(
        verbose_name='Sobrenome',
        max_length=80,
        blank=True,
        help_text='Sobrenome do usuário'
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
