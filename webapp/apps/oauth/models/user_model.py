import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from oauth.constants import UserGroup


class AccountManager(BaseUserManager):
    def create_user(
        self, email, username, password=None
    ):  # Passing email and username b/c both are required when signing up
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")

        # normalize_email converts all emails to lowercase, inherited from BaseUserManager
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    # Required Abstract Base User Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    account_type = models.CharField(max_length=30, default=UserGroup.USER.value)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Custom Abstract Base User Fields
    first_name = models.CharField(max_length=60)

    USERNAME_FIELD = "email"  # Field used to login, can be username/email/...
    REQUIRED_FIELDS = [
        "username",
    ]  # Fields required when registering

    objects = AccountManager()

    def __str__(self):
        return f"{self.email}"

    # Required permission function
    def has_perm(self, perm, obj=None):
        return self.is_admin  # need to change

    def has_module_perms(self, app_label):
        return True

    # Custom function overrides
