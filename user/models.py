from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.save()
        return user

    def create_superuser(self, email, **kwargs):
        email = self.normalize_email(email)
        confirmation_code = 000000
        user = self.model(email=email, is_staff=True, is_superuser=True,
                          confirmation_code=confirmation_code,
                          **kwargs)
        user.save()
        return user


class CustomUser(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_TYPE_CHOICES = (
        (USER, 'Normal User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    )
    role = models.CharField(max_length=100, choices=USER_TYPE_CHOICES,
                            default='user')
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=100,)
    bio = models.TextField(blank=True, null=True,)
    first_name = models.CharField(max_length=100, blank=True, null=True,)
    last_name = models.CharField(max_length=100, blank=True, null=True,)
    confirmation_code = models.CharField(max_length=100, blank=True,
                                         null=True,)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username', ]
