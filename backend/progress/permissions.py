from rest_framework.permissions import BasePermission


class IsEnrolledStudent(BasePermission):
    message = 'You must be enrolled in this course.'

    def has_object_permission(self, request, view, obj):
        if request.user.role == request.user.Role.ADMIN:
            return True
        if request.user.role == request.user.Role.INSTRUCTOR:
            return obj.course.instructor == request.user
        return obj.student == request.user