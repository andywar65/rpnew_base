# Generated by Django 2.2.7 on 2020-01-07 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('direzione', '0005_auto_20200107_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='society',
            name='executive',
            field=models.ManyToManyField(related_name='society_executive', to=settings.AUTH_USER_MODEL, verbose_name='Dirigenti'),
        ),
        migrations.AlterField(
            model_name='society',
            name='president',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='society_president', to=settings.AUTH_USER_MODEL, verbose_name='Presidente'),
        ),
        migrations.AlterField(
            model_name='society',
            name='trainers',
            field=models.ManyToManyField(related_name='society_trainers', to=settings.AUTH_USER_MODEL, verbose_name='Istruttori'),
        ),
    ]