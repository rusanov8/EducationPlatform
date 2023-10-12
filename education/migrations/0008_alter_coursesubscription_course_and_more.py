# Generated by Django 4.2.5 on 2023-10-08 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('education', '0007_coursesubscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesubscription',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe', to='education.course'),
        ),
        migrations.AlterField(
            model_name='coursesubscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe', to=settings.AUTH_USER_MODEL),
        ),
    ]