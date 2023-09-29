from django.db import models

from education.models import Course, Lesson
from users.models import User


class Payment(models.Model):

    PAYMENT_METHODS = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='payments')
    date = models.DateField(verbose_name='Дата оплаты')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='payment')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name='payment')

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')

    def __str__(self):
        if self.course:
            return f'Платеж от {self.user} за курс "{self.course}"'
        else:
            return f'Платеж от {self.user} за урок "{self.lesson}"'

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        db_table = 'Платежи'
        ordering = ('-date',)

