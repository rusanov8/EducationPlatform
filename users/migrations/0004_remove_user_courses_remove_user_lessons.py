# Generated by Django 4.2.5 on 2023-10-03 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_courses_alter_user_lessons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='user',
            name='lessons',
        ),
    ]
