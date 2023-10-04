from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from education.models import Course, Lesson
from education.permissions import IsModerator, IsCourseOwner, IsLessonOwner
from education.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):

        if self.action == 'list':
            # Разрешить просматривать курсы для всех, включая модераторов и владельцев
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            # Просмотр отдельного курса разрешен только модераторам или владельцам
            permission_classes = [IsModerator | IsCourseOwner]
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

    # Просмотр списка уроков разрешен авторизованным пользователям, включая модераторов и владельцев уроков.
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    # Просмотр отдельного урока разрешен только модераторам или владельцам
    permission_classes = [IsModerator | IsLessonOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    # Редактирование уроков разрешено только модераторы и владельцы уроков
    permission_classes = [IsModerator | IsLessonOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

    # Удаление уроков разрешено только владельцам уроков.
    permission_classes = [IsLessonOwner]



