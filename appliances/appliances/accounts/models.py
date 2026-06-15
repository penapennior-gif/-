from django.db import models
from django.contrib.auth.models import User
from datetime import date

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name='Фото')
    position = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='Возраст')
    hired_date = models.DateField(null=True, blank=True, verbose_name='Дата устройства на работу')
    service_location = models.CharField(max_length=255, blank=True, verbose_name='Место прохождения службы')
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f'Профиль {self.user.username}'
    
    @property
    def service_years(self):
        """Вычисляет срок службы в годах"""
        if self.hired_date:
            return (date.today() - self.hired_date).days // 365
        return 0


class AccessCode(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='access_codes',
        verbose_name='Пользователь',
        help_text='Пользователь, которому назначен этот код. Оставьте пустым для общего кода.'
    )
    name = models.CharField(max_length=150, blank=True, verbose_name='Название кода')
    code = models.CharField(max_length=60, unique=True, verbose_name='Код доступа')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Код доступа'
        verbose_name_plural = 'Коды доступа'

    def __str__(self):
        return f'{self.name or self.code} ({self.user.username if self.user else "общий"})'

