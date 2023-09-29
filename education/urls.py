from django.urls import path
from rest_framework.routers import DefaultRouter

from education.apps import EducationConfig
from education.views import CourseViewSet, LessonCreateApiView, LessonListApiView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')


urlpatterns = [
    path('lessons/create', LessonCreateApiView.as_view(), name='lesson-create'),
    path('lessons/', LessonListApiView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lessons/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson-delete'),



] + router.urls


