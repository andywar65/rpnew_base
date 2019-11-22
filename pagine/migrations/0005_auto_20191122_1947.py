# Generated by Django 2.2.7 on 2019-11-22 18:47

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagine', '0004_auto_20191122_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Descrizione'),
        ),
        migrations.AlterField(
            model_name='location',
            name='gmap_embed',
            field=models.URLField(blank=True, help_text="Dal menu di Google Maps seleziona 'Condividi/incorpora',                    copia il link e incollalo qui", max_length=500, null=True, verbose_name='Incorpora Google Map'),
        ),
        migrations.AlterField(
            model_name='location',
            name='gmap_link',
            field=models.URLField(blank=True, help_text="Dal menu di Google Maps seleziona 'Condividi/link',                    copia il link e incollalo qui", null=True, verbose_name='Link di Google Map'),
        ),
    ]
