from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='rusanov.egor@bk.ru',
            first_name='Egor',
            last_name='Rusanov',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('education88')
        user.save()

