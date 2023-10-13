from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from education.models import Course, Lesson, CourseSubscription
from education.paginators import BasePaginator
from education.permissions import IsModerator, IsCourseOwner, IsLessonOwner
from education.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer

from education.tasks import send_update_email


class CourseViewSet(viewsets.ModelViewSet):
    """
    Manage courses, including creation, listing, and updates.

    This viewset allows you to perform various operations related to courses,
    such as creating new courses, listing available courses, and updating course details.
    """

    queryset = Course.objects.select_related('owner').prefetch_related('lessons')
    pagination_class = BasePaginator

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_serializer_class(self):
        if self.request.query_params.get('detail') == 'True':
            return CourseDetailSerializer
        else:
            return CourseSerializer

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsModerator, IsCourseOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated & ~IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsCourseOwner]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        instance = serializer.save()
        send_update_email.delay(instance)



class LessonCreateApiView(generics.CreateAPIView):
    """
    Create new lessons within a course.

    This view allows authenticated users to create new lessons within a course.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & ~IsModerator]


class LessonListApiView(generics.ListAPIView):
    """
    List available lessons.

    This view allows authenticated users to list all available lessons.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = BasePaginator

    permission_classes = [IsAuthenticated]


class LessonListForCourseAPIView(generics.ListAPIView):
    """
    List lessons for a specific course.

    This view allows authenticated users to list lessons associated with a specific course.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = BasePaginator

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        queryset = Lesson.objects.filter(course_id=course_id)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Retrieve lesson details.

    This view allows users to retrieve details of a specific lesson.
    Access is granted to moderators and lesson owners.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = [IsModerator | IsLessonOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Update lesson details.

    This view allows moderators and lesson owners to update lesson details.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = [IsModerator | IsLessonOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Delete a lesson.

    This view allows lesson owners to delete a lesson.
    """
    queryset = Lesson.objects.all()

    # Удаление уроков разрешено только владельцам уроков.
    permission_classes = [IsLessonOwner]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_to_course(request, pk):
    """
    Subscribe to a course.

    This function allows authenticated users to subscribe to a specific course.
    """

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
        return Response({'detail': f'Подписка на курс {course.title} оформлена'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsubscribe_from_course(request, pk):
    """
    Unsubscribe from a course.

    This function allows authenticated users to unsubscribe from a specific course.
    """

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
