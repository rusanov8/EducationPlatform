from django.contrib.auth.models import AbstractUser
from django.db import models

from education.models import Course, Lesson


class User(AbstractUser):

    username = None

    email = models.EmailField(verbose_name='Почта', unique=True)
    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', blank=True, null=True)

    courses = models.ManyToManyField(Course, related_name='users', blank=True, verbose_name='Курсы')
    lessons = models.ManyToManyField(Lesson, related_name='users', blank=True, verbose_name='Уроки')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'



