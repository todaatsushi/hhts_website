from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='ユーザー')
    name = models.CharField(max_length=50, verbose_name='名前')
    about = models.TextField(verbose_name='個人情報')
    image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics', verbose_name='写真')
    role = models.CharField(max_length=50, default='Tour Guide', verbose_name='役割')

    def __str__(self):
        return f'{self.name} - {self.user.username}'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        dims = (200, 200)

        if img.height > 200 or img.width > 200:
            img.thumbnail(dims)
            img.save(self.image.path)
