from rest_framework.test import APITestCase
from rest_framework import status

from education.models import Lesson, Course, User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        # Добавляем пользователя в тестовую БД
        self.user = User.objects.create(
            email='test@test.ru',
            password='testpassword',
        )
        self.client.force_authenticate(user=self.user)

        # Добавляем курс в тестовую БД
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            owner=self.user
        )

        self.lesson_data = {
            'title': 'Тестовый урок',
            'description': 'Урок для теста',
            'video_url': 'https://www.youtube.com/watch?v=2JGbRnJfG0g',
            'course': self.course
        }

    def test_create_lesson(self):
        self.lesson_data['course'] = self.course.id

        response = self.client.post(
            '/lessons/create', self.lesson_data
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_get_lesson_list(self):
        lesson = Lesson.objects.create(**self.lesson_data)

        response = self.client.get(
            '/lessons/'
        )

        # Сравниваем статуты ответов
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Сравниваем результат запроса
        response_data = response.json()['results']
        expected_data = [{'id': lesson.id, 'title': 'Тестовый урок', 'description': 'Урок для теста',
                          'video_url': 'https://www.youtube.com/watch?v=2JGbRnJfG0g', 'course': self.course.id,
                          'preview': None}]
        self.assertEqual(response_data, expected_data)

    def test_get_lesson_list_for_course(self):
        lesson = Lesson.objects.create(**self.lesson_data)

        response = self.client.get(
            f'/courses/{self.course.id}/lessons/'
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        response_data = response.json()['results']  # Используем ['results'] чтобы учесть пагинацию
        expected_data = [{'id': lesson.id, 'title': 'Тестовый урок', 'description': 'Урок для теста',
                          'video_url': 'https://www.youtube.com/watch?v=2JGbRnJfG0g', 'course': self.course.id,
                          'preview': None}]
        self.assertEqual(response_data, expected_data)

    def test_get_lesson_detail(self):
        lesson = Lesson.objects.create(**self.lesson_data)

        response = self.client.get(
            f'/lessons/{lesson.id}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        expected_data = {'id': lesson.id, 'title': 'Тестовый урок', 'description': 'Урок для теста',
                         'video_url': 'https://www.youtube.com/watch?v=2JGbRnJfG0g', 'course': self.course.id,
                         'preview': None}

        self.assertEqual(response_data, expected_data)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(**self.lesson_data)

        updated_data = {
            'title': 'Обновленный урок',
            'description': 'Новое описание',
            'video_url': 'https://www.youtube.com/watch?v=12323',
            'course': self.lesson_data['course'].id
        }

        response = self.client.put(f'/lessons/update/{lesson.id}/', updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(**self.lesson_data)

        response = self.client.delete(f'/lessons/delete/{lesson.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())
