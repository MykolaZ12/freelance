from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from freelance.users.managers import UserManager


class User(AbstractBaseUser):
    USER_TYPES = (
        ("Default", 'Default'),
        ('Customer', 'Customer'),
        ('Executor', 'Executor'),
    )

    user_type = models.CharField('User type', choices=USER_TYPES, default="Default", max_length=10)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=150, blank=True, null=True)
    last_name = models.CharField('last name', max_length=150, blank=True, null=True)
    phone_number = models.CharField('phone number', max_length=15, blank=True, null=True)

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.')
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    is_admin = models.BooleanField(
        'superuser status',
        default=False,
        help_text='Designates whether this user can be a super user.'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
