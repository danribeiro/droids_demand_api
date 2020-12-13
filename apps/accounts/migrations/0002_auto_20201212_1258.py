# Generated by Django 3.1.4 on 2020-12-12 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, help_text='Nome do usuário', max_length=80, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, help_text='Sobrenome do usuário', max_length=80, verbose_name='Sobrenome'),
        ),
    ]
