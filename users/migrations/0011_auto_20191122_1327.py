# Generated by Django 2.2.7 on 2019-11-22 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_usermessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='course',
        ),
        migrations.DeleteModel(
            name='CourseSchedule',
        ),
    ]