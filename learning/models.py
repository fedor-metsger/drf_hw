
from django.db import models

from users.models import User

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(verbose_name='изображение', null=True, blank=True)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'Course({self.title})'
        # return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(verbose_name='изображение', null=True, blank=True)
    video = models.CharField(max_length=150, verbose_name='видео', null=True, blank=True)

    def __str__(self):
        return f'Lesson({self.title})'
        # return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'