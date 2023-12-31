# Generated by Django 4.2.5 on 2023-09-28 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_alter_lesson_course'),
        ('users', '0002_user_courses_user_lessons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='users', to='education.course', verbose_name='Курсы'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lessons',
            field=models.ManyToManyField(blank=True, related_name='users', to='education.lesson', verbose_name='Уроки'),
        ),
    ]
