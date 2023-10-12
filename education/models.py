from django.db import models

from users.models import User


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(max_length=55, verbose_name='Название')
    preview = models.ImageField(upload_to='course_previews/', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name='Владелец', default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        db_table = 'courses'


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='Превью', blank=True, null=True)
    video_url = models.URLField(verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='lessons',)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        db_table = 'lessons'


class CourseSubscription(models.Model):
    """Модель подписки"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribe')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscribe')
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f'Подписка пользователя {self.user.email} на курс {self.course.title}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        db_table = 'course_subscription'
        unique_together = ('user', 'course')






