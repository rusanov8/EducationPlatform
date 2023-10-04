from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='moderator_1@bk.ru',
            first_name='Moderator',
            last_name='Moderatorov',
            is_staff=True,
        )

        user.set_password('education88')
        user.save()
