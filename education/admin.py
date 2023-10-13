from django.contrib import admin

from education.models import Course, Lesson, CourseSubscription


admin.site.register(Lesson)

admin.site.register(CourseSubscription)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

