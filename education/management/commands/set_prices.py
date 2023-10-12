from django.core.management import BaseCommand
from education.models import Course

from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Set random prices for all courses'

    def handle(self, *args, **options):

        courses = Course.objects.all()

        for course in courses:
            random_price = Decimal(random.uniform(500, 10000)).quantize(Decimal('0.01'))

            course.price = random_price
            course.save()

            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated price for course {course.title} to {random_price}'))
