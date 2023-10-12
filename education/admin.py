from django.contrib import admin

from education.models import Course, Lesson, CourseSubscription


admin.site.register(Course)

admin.site.register(Lesson)

admin.site.register(CourseSubscription)

