# Generated by Django 3.0.2 on 2020-02-16 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_usermessage_privacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='privacy',
            field=models.BooleanField(default=False),
        ),
    ]
