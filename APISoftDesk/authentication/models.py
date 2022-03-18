from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):

    groups = models.ForeignKey(Group, related_name='user_role', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username
# Create your models here.


