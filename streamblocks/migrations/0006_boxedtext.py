# Generated by Django 3.0.2 on 2020-02-07 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamblocks', '0005_linkablelist'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxedText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('success', 'Verde'), ('warning', 'Giallo'), ('danger', 'Rosso')], default='success', max_length=10, verbose_name='Colore')),
                ('body', models.TextField(help_text='Accetta tag HTML', null=True, verbose_name='Testo')),
            ],
            options={
                'verbose_name': 'Testo in un box',
                'verbose_name_plural': 'Testi in un box',
            },
        ),
    ]