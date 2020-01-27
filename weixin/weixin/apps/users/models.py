from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
class User(AbstractBaseUser):
    """
    User basic information
    """

    # We don't store password here
    password = None

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)
    birthday = models.DateTimeField(null=True)
    gender = models.CharField(max_length=16, null=True)
    avatar = models.CharField(max_length=1024, null=True)
    signature = models.CharField(max_length=4096, null=True)
    phone = models.BigIntegerField(unique=True)
    email = models.CharField(max_length=128, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_robot = models.BooleanField(default=False)
    is_boss = models.BooleanField(default=False)                             # 是否是大老板
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    forbidden_end_time = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('is_robot', 'id',)

    def __str__(self):
        return ":".join([str(self.id), self.name])