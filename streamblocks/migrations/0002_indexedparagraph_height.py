# Generated by Django 3.0.2 on 2020-02-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamblocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexedparagraph',
            name='height',
            field=models.CharField(choices=[('4', 'Medio'), ('5', 'Piccolo'), ('6', 'Molto piccolo')], default='4', max_length=1),
        ),
    ]
