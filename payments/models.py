from django.db import models

from education.models import Course, Lesson
from users.models import User


class Payment(models.Model):

    PAYMENT_METHODS = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='payments')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='payment')

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты', default=0)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')
    payment_date = models.DateField(auto_now_add=True, verbose_name='Дата платежа')

    def __str__(self):
        return f'Платеж от {self.user} за курс "{self.course}"'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        db_table = 'payments'
        ordering = ('-payment_date',)

