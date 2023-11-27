from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise TypeError('Invalid username')
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **kwargs):
        if not password:
            raise TypeError('password no')
        user = self.create_user(username, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    ROLE = (
        ("receiver", "receiver"),
        ("specialist", "specialist"),
        ("accountant", "accountant"),
        ("client", "client"),
        ("uz_standard", "uz_standard"),
        ("inspector_1", "inspector_1"),
        ("inspector_2", "inspector_2"),
    )
    username = models.CharField(max_length=64, unique=True)
    full_name = models.CharField(max_length=350, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    role = models.CharField(choices=ROLE, max_length=25, default='receiver')

    USERNAME_FIELD = 'username'
    objects = AccountManager()

    def __str__(self):
        return self.username
