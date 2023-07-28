
from django.db import models

from users.models import User

# Create your models here.
class Breed(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'Breed({self.name})'
        # return self.name

    class Meta:
        verbose_name = 'порода'
        verbose_name_plural = 'породы'

class Dog(models.Model):
    name = models.CharField(max_length=150, verbose_name='кличка')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name="dogs")
    photo = models.ImageField(verbose_name='фотография', null=True, blank=True)
    birthdate = models.DateField(verbose_name='дата рождения', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False, verbose_name='публичная', null=True, blank=True)
    price = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f'Dog({self.name, self.breed})'
        # return self.name

    class Meta:
        verbose_name = 'собака'
        verbose_name_plural = 'собаки'

class Ancestor(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='кличка')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    birthdate = models.DateField(verbose_name='дата рождения', null=True, blank=True)

    def __str__(self):
        return f'Ancestor({self.name, self.breed})'
        # return self.name

    class Meta:
        verbose_name = 'предок'
        verbose_name_plural = 'предки'
