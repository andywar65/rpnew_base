from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import *

class User(AbstractUser):
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        try:
            memb = Member.objects.get(user_id = self.id)
            return
        except:
            memb = Member.objects.create(user = self, )
            memb.save()
            return

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True, editable=False)
    sector = models.CharField(max_length = 4, choices = SECTOR,
        default = '0-NO')
    parent = models.ForeignKey(User, on_delete = models.SET_NULL,
        blank = True, null = True, related_name = 'member_parent')

    class Meta:
        verbose_name = 'Iscritto'
        verbose_name_plural = 'Iscritti'
