from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from education.models import Course, Lesson, CourseSubscription
from education.paginators import BasePaginator
from education.permissions import IsModerator, IsCourseOwner, IsLessonOwner
from education.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = BasePaginator


    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            # Разрешить просматривать курсы для всех, включая модераторов и владельцев
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            # Разрешить редактировать курсы только модераторам и владельцам
            permission_classes = [IsModerator, IsCourseOwner]
        elif self.action == 'create':
            # Разрешить создавать курсы только авторизованным пользователям
            permission_classes = [IsAuthenticated & ~IsModerator]
        elif self.action == 'destroy':
            # Разрешить удалять курсы только владельцам
            permission_classes = [IsCourseOwner]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]


class LessonCreateApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    # Создание уроков разрешено только авторизованным пользователям
    permission_classes = [IsAuthenticated & ~IsModerator]


class LessonListApiView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = BasePaginator

    # Просмотр списка уроков разрешен авторизованным пользователям, включая модераторов и владельцев уроков.
    permission_classes = [IsAuthenticated]


class LessonListForCourseAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = BasePaginator

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        queryset = Lesson.objects.filter(course_id=course_id)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    # Просмотр отдельного урока разрешен только модераторам или владельцам
    permission_classes = [IsModerator | IsLessonOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    # # Редактирование уроков разрешено только модераторы и владельцы уроков
    # permission_classes = [IsModerator | IsLessonOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

    # Удаление уроков разрешено только владельцам уроков.
    permission_classes = [IsLessonOwner]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_to_course(request, pk):
    """Контроллер для подписки на курс"""

    try:
        course = Course.objects.get(pk=pk)

    except Course.DoesNotExist:
        return Response({"detail": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)

    try:
        subscription = CourseSubscription.objects.get(user=request.user, course=course)
        if subscription.is_subscribed:
            return Response({'detail': 'Вы уже подписаны на этот курс.'})
        else:
            subscription.is_subscribed = True
            subscription.save()
            return Response({'detail': f'Подписка на курс {course.title} оформлена'}, status=status.HTTP_201_CREATED)

    except CourseSubscription.DoesNotExist:
        subscription = CourseSubscription.objects.create(user=request.user, course=course)
        subscription.is_subscribed = True
        subscription.save()
        return Response({'detail': f'Подписка на курс {course.title } оформлена'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsubscribe_from_course(request, pk):
    """Контроллер для отписки от курса"""

    try:
        course = Course.objects.get(pk=pk)

    except Course.DoesNotExist:
        return Response({"detail": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)

    try:
        subscription = CourseSubscription.objects.get(user=request.user, course=course)
        if subscription.is_subscribed:
            subscription.is_subscribed = False
            subscription.save()
            return Response({'detail': f'Отписка от курса {course.title}'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'Вы уже отписаны от курса {course.title}'}, status=status.HTTP_200_OK)

    except CourseSubscription.DoesNotExist:
        return Response({'detail': 'Вы не подписаны на курс {course.title}.'}, status=status.HTTP_400_BAD_REQUEST)


