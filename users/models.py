from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='почта')
    is_active = models.BooleanField(
        default=False,
        verbose_name='активен')

    verification_token = models.CharField(
        **NULLABLE,
        max_length=20,
        verbose_name='токен')
    phone = models.CharField(
        **NULLABLE,
        unique=True,
        verbose_name='телефон')
    avatar = models.ImageField(
        **NULLABLE,
        upload_to='avatar',
        verbose_name='аватар')
    country = models.CharField(
        **NULLABLE,
        max_length=150,
        verbose_name='страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
