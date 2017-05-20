from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
# Create your models here.


class WHU(models.Model):
    user = models.OneToOneField(User)
    is_teacher = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('has_publish_signin', 'Can publish'),
            ('has_delete_signin', 'Delete Sign in'),
        )

    def __str__(self):
        return self.user.username

class SignIn(models.Model):

    group = models.ForeignKey(Group)
    is_time = models.BooleanField(default=False)
    publish = models.DateTimeField(default=timezone.now)
