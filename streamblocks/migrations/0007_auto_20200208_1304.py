# Generated by Django 3.0.2 on 2020-02-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamblocks', '0006_boxedtext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxedtext',
            name='body',
            field=models.TextField(null=True, verbose_name='Testo'),
        ),
    ]
