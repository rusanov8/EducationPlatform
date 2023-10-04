from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()


class IsCourseOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем курса
        return request.user == obj.owner


class IsLessonOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем курса, к которому принадлежит урок (владельцем урока)
        return request.user == obj.course.owner

