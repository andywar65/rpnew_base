# Generated by Django 2.2.7 on 2019-12-21 09:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pagine', '0037_auto_20191221_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 21, 9, 54, 59, 63261, tzinfo=utc), verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 21, 9, 54, 59, 63261, tzinfo=utc), verbose_name='Quando'),
        ),
        migrations.AlterField(
            model_name='eventupgrade',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 21, 9, 54, 59, 63261, tzinfo=utc), verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='userupload',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 21, 9, 54, 59, 63261, tzinfo=utc), verbose_name='Data'),
        ),
    ]