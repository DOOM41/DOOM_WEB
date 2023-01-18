# Django
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    ImageField,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

# Apps
from abstracts.validators import APIValidator
from abstracts.models import AbstractsDateTime


class CustomUserManager(
    BaseUserManager
):
    def create_user(self,
                    email: str,
                    login: str,
                    pin: str,
                    password: str
                    ) -> 'CustomUser':
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
            is_staff=True,
            email=self.normalize_email(email),
            login=login,
            password=password
        )
        user.is_superuser: bool = True
        user.is_active: bool = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def get_undeleted_user(self,id) -> 'CustomUser':
        """Get undeleted user"""
        try:
            user: CustomUser = self.get(
                id=id,
                deleted_at=None
            )
            return user
        except:
            raise APIValidator(
                'Данный пользователь не найден',
                'message',
                '400',
            )

    def set_user(self, user: 'CustomUser', nick, password):
        user.set_password(password)
        user.verificated_code = None
        user.is_active = True
        user.nick_name = nick
        user.save()
        return user


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
    nick_name = CharField(
        'Никнейм',
        max_length=100,
    )
    avatar = ImageField(upload_to='media/avatar')
    is_active: BooleanField = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    verificated_code = CharField(
        'Код подтверждения', max_length=5, null=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']
    objects = CustomUserManager()

    class Meta:
        ordering = (
            'created_at',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
