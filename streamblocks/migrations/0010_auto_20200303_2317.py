# Generated by Django 3.0.2 on 2020-03-03 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streamblocks', '0009_gallery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gallery',
            options={'verbose_name': 'Galleria di immagini', 'verbose_name_plural': 'Galleria di immagini'},
        ),
        migrations.AlterModelOptions(
            name='linkablelist',
            options={'verbose_name': 'Lista con link', 'verbose_name_plural': 'Lista con link'},
        ),
    ]
