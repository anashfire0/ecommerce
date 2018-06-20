from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Guest(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, staff=False, admin=False, active=True):
        if not email:
            raise ValueError('Users must have an email address.')
        if not password:
            raise ValueError('Users must have a password.')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.staff = staff
        user.active = active
        user.admin = admin
        user.full_name = full_name
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(email, password, full_name, staff=True)
        return user

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email, full_name, password, staff=True, admin=True)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    active = models.BooleanField(default=True)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    # username and password are required by default
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin
