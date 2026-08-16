from rest_framework.permissions import BasePermission


class IsQuizInstructorOrAdmin(BasePermission):
    message = 'Only the quiz instructor or admin can perform this action.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == user.Role.ADMIN:
            return True
        if user.role == user.Role.INSTRUCTOR:
            return obj.course.instructor == user
        return False


class IsAssignmentInstructorOrAdmin(BasePermission):
    message = 'Only the assignment instructor or admin can perform this action.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == user.Role.ADMIN:
            return True
        if user.role == user.Role.INSTRUCTOR:
            return obj.course.instructor == user
        return False