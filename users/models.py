from django.db import models
from django.contrib.auth.models import AbstractUser

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
