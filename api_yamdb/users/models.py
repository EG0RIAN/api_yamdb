from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    bio = models.CharField(
        max_length=140,
        verbose_name='Информация о пользователе',
        help_text='О себе'
    )
    role = models.CharField(
        max_length=16,
        choices=ROLES,
        default='user',
    )
