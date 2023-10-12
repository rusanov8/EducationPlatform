
from django.core.management.base import BaseCommand
from faker import Faker
from users.models import User
from education.models import Course, Lesson

fake = Faker()

class Command(BaseCommand):
    help = 'Create 100 test users with courses and lessons'

    def handle(self, *args, **kwargs):
        for _ in range(10):
            user = User.objects.create(
                email=fake.email(),
                password=fake.password(),
            )

            for _ in range(10):
                course_title = fake.sentence()
                if len(course_title) > 55:
                    course_title = course_title[:55]

                course = Course.objects.create(
                    title=course_title,
                    description=fake.paragraph(),
                    owner=user,
                )

                for _ in range(10):
                    Lesson.objects.create(
                        title=fake.sentence(),
                        description=fake.paragraph(),
                        video_url=fake.url(),
                        course=course,
                    )

            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.email}'))