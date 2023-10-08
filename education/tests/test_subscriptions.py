from rest_framework.test import APITestCase
from rest_framework import status

from education.models import CourseSubscription, Course, User


class SubscriptionTestCase(APITestCase):

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

    def test_subscription(self):
        response = self.client.post(
            f'/courses/{self.course.id}/subscribe'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(CourseSubscription.objects.all().exists())

        self.assertTrue(CourseSubscription.objects.get(id=1).is_subscribed)

        expected_response_data = {'detail': f'Подписка на курс {self.course.title} оформлена'}
        self.assertEqual(response.data, expected_response_data)

        # Тесты на повторную попытку подписки
        response_duplicate_sub = self.client.post(f'/courses/{self.course.id}/subscribe')

        expected_response_duplicate_data = {'detail': 'Вы уже подписаны на этот курс.'}

        self.assertEqual(response_duplicate_sub.data, expected_response_duplicate_data)


    def test_unsubscription(self):

        response_sub = self.client.post(
            f'/courses/{self.course.id}/subscribe'
        )

        response_unsub = self.client.post(
            f'/courses/{self.course.id}/unsubscribe'
        )

        self.assertEqual(response_unsub.status_code, status.HTTP_200_OK)

        self.assertFalse(response_unsub.data.get('is_subscribed'))
