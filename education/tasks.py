from celery import shared_task
from django.core.mail import send_mail
from config import settings
from users.models import User

from datetime import datetime, timedelta


@shared_task
def send_update_email(instance):

    subscribed_users = User.objects.filter(subscribe__course=instance, subscribe__is_subscribed=True)

    send_mail(
        subject=f'Курс {instance.title} обновлен',
        message=f'Курс {instance.title} был обновлен. Проверьте новый материал: http://127.0.0.1:8000/courses/{instance.pk}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email for user in subscribed_users]
    )


def check_users_activity():

    today_date = datetime.now().date()
    days_threshold = 30

    users_to_update = User.objects.filter(
        last_login__date__lt=today_date - timedelta(days=days_threshold)
    )

    users_to_update.update(is_active=False)
