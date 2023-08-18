from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, phone_number, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not phone_number:
            raise ValueError("The Phone Number field is required")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password):
        """Create and return a new superuser."""
        user = self.create_user(phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    phone_number = PhoneNumberField(unique=True)
    invite_code = models.CharField(max_length=6, null=True, blank=True)
    activated_invite_code = models.BooleanField(null=True, blank=True)
    code = models.CharField(max_length=4, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return f"{self.phone_number}"