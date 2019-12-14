# Generated by Django 2.2.7 on 2019-12-14 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_usermessage_notice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessage',
            name='notice',
            field=models.CharField(choices=[('SPAM', 'Da inviare'), ('DONE', 'Già inviata')], default='SPAM', max_length=4, verbose_name='Notifica via email'),
        ),
    ]
