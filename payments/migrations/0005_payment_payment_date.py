# Generated by Django 4.2.5 on 2023-10-10 04:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_remove_payment_lesson_alter_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата платежа'),
            preserve_default=False,
        ),
    ]
