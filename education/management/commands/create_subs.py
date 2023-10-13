from django.core.management.base import BaseCommand
from education.models import Course, CourseSubscription
from users.models import User



class Command(BaseCommand):
    help = 'Создать подписки для пользователей'

    def handle(self, *args, **options):

        users = User.objects.exclude(id=101)
        courses = Course.objects.all()

        for user in users:
            random_courses = courses.order_by('?')[:2]  # Выбираем два случайных курса

            for course in random_courses:
                subscription, created = CourseSubscription.objects.get_or_create(user=user, course=course, defaults={'is_subscribed': True})

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Создана подписка пользователя {user.email} на курс {course.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Подписка пользователя {user.email} на курс {course.title} уже существует'))

        self.stdout.write(self.style.SUCCESS('Подписки успешно созданы'))