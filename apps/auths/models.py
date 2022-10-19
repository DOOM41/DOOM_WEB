# Django
from django.db.models import (
    EmailField,
    CharField,
    QuerySet,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

# Rest
from rest_framework.response import Response

# Apps
from abstracts.validators import APIValidator
from abstracts.models import AbstractsDateTime


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, login: str, pin: str, password: str) -> 'CustomUser':
        if not email:
            raise ValidationError('Email required')
        try:
            user: 'CustomUser' = self.model(
                email=self.normalize_email(email),
                login=login,
                password=password,
                verificated_code=pin,
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            raise APIValidator(
                'Данный пользователь уже существует',
                'message',
                '400',
            )

    def create_superuser(self, email: str, login, password: str) -> 'CustomUser':
        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            login=login,
            password=password
        )
        user.is_superuser: bool = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_undeleted_user(self, email: str) -> QuerySet['CustomUser']:
        """Get undeleted user"""
        try:
            users: QuerySet[CustomUser] = self.get(
                email=email,
                deleted_at=None
            )
            return users
        except:
            return Response(
                data={'message': 'Такой пользователь не найден'},
                status=404
            )


class CustomUser(
    AbstractBaseUser,
    PermissionsMixin,
    AbstractsDateTime
):
    email = EmailField(
        'Почта/Логин',
        unique=True,
        null=False
    )
    login = CharField(
        'Номер телефона',
        unique=True,
        max_length=11,
    )
    verificated_code = CharField('Код подтверждения', max_length=5, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']
    objects = CustomUserManager()

    class Meta:
        ordering = (
            'created_at',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
