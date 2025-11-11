from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь',  on_delete=models.CASCADE)
    nickname = models.CharField(verbose_name='Никнейм', max_length=50, unique=True, null=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'