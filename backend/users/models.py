from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model, validators
from django.db import models


class CustomUser(AbstractUser):

    username = models.TextField(
        max_length=150,
        unique=True,
        validators=[validators.UnicodeUsernameValidator],
        verbose_name='Логин',
        help_text='Логин'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Введите электронный адрес'
    )
    first_name = models.TextField(
        max_length=150,
        verbose_name='Имя',
        help_text='Введите имя'
    )
    last_name = models.TextField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Введите фамилию'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            ),
        )


User = get_user_model()
