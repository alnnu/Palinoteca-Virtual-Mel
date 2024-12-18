from django.db import models

import uuid
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        # see if email is valid
        email = self.normalize_email(email)


        user = self.model(email=email, name=name, **extra_fields)


        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=False, name=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    # set de login info
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

class ResetPasswordToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    dateToExpire = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()