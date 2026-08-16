from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class Role(models.TextChoices):
    ADMIN = 'ADMIN', _('Admin')
    INSTRUCTOR = 'INSTRUCTOR', _('Instructor')
    STUDENT = 'STUDENT', _('Student')


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('full name'), max_length=255)
    role = models.CharField(
        _('role'),
        max_length=12,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    is_active = models.BooleanField(_('active'), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.name} ({self.email})'

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser

    @property
    def is_instructor(self):
        return self.role == Role.INSTRUCTOR

    @property
    def is_student(self):
        return self.role == Role.STUDENT