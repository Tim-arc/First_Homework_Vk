from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь',  on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f'Профиль пользователя #{self.user_id}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'