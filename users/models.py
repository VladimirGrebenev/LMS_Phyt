from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from uuid import uuid4
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class UserRoles(models.TextChoices):
    MODERATOR = 'moderator', _('moderator')
    STUDENT = 'student', _('student')
    TEACHER = 'teacher', _('teacher')

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель User, поле email при аутентификации"""
    id = models.UUIDField(default=uuid4, primary_key=True, verbose_name='id')
    first_name = models.CharField(max_length=64, verbose_name='firstname')
    last_name = models.CharField(max_length=64, verbose_name='lastname')
    user_name = models.CharField(max_length=64, verbose_name='username')
    email = models.EmailField(max_length=256, unique=True, blank=False,
                              verbose_name='email')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Edited")
    deleted = models.BooleanField(default=False)
    role = models.CharField(choices=UserRoles.choices, max_length=10,
                            verbose_name='user_role',
                            default=UserRoles.STUDENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.user_name}"

    def delete(self, *kwargs):
        """Из базы данных пользователей не удаляем, просто помечаем
        удалёнными"""
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = ("Пользователь Сервиса")
        verbose_name_plural = ("Пользователи Сервиса")
        ordering = ("-date_joined",)
