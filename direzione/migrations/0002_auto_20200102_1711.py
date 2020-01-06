# Generated by Django 2.2.7 on 2020-01-02 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direzione', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conventionupload',
            options={'verbose_name': 'File', 'verbose_name_plural': 'Files'},
        ),
        migrations.AddField(
            model_name='convention',
            name='slug',
            field=models.SlugField(editable=False, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Descrizione'),
        ),
    ]