from PIL import Image

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an name')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.TextField(max_length=24, blank=False, unique=True)
    email = models.EmailField(unique=True, blank=False)
    avatar = models.ImageField(upload_to='avatars/', default='def_avatar.jpg')
    bio = models.TextField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            max_size = 50  # maximum allowed size
            if img.height > max_size or img.width > max_size:
                img.thumbnail((max_size, max_size))
                img.save(self.avatar.path)


class Activation(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def expired(self):
        expiration_time = timezone.now() - timezone.timedelta(days=1)
        return self.created_at < expiration_time
