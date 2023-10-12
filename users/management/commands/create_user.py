from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='test@test.com',
            first_name='Test',
            last_name='Testov',
        )

        user.set_password('education88')
        user.save()

