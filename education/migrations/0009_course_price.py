# Generated by Django 4.2.5 on 2023-10-10 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0008_alter_coursesubscription_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Стоимость'),
        ),
    ]
