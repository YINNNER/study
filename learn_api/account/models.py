from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
# Create your models here.


class WHU(models.Model):
    user = models.OneToOneField(User)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class SignIn(models.Model):

    group = models.ForeignKey(Group)
    is_time = models.BooleanField(default=False)
    publish = models.DateTimeField(default=timezone.now)
