from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUser(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_TYPE_CHOICES = (
        (USER, 'Normal User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    )
    role = models.CharField(max_length=100, choices=USER_TYPE_CHOICES, default='user')
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=100,)
    bio = models.TextField()
    first_name = models.CharField(max_length=100,)
    last_name = models.CharField(max_length=100,)
    confirmation_code = models.CharField(max_length=100,)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=True, is_superuser=True,
                          **kwargs)
        user.set_password(password)
        user.save()
        return user