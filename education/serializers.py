from rest_framework import serializers

from education.models import Course, Lesson, CourseSubscription
from education.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            UrlValidator(field='video_url')
        ]


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ('title', 'owner', 'preview', 'description', 'lessons', 'lessons_count', 'is_subscribed')

        extra_kwargs = {
            'preview': {'required': False}
        }

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, instance):
        request = self.context.get('request')
        user = request.user if request else None
        try:
            subscription = CourseSubscription.objects.get(user=user, course=instance)
            return subscription.is_subscribed
        except CourseSubscription.DoesNotExist:
            return False







