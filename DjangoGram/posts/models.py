from django.db import models
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from DjangoGram.accounts.models import User

from PIL import Image


class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=AnonymousUser().pk)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.cover:
            img = Image.open(self.cover.path)
            max_size = 500  # maximum allowed size
            if img.height > max_size or img.width > max_size:
                img.thumbnail((max_size, max_size))
                img.save(self.cover.path)
