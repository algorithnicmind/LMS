from rest_framework.permissions import BasePermission


class IsInstructorOrAdmin(BasePermission):
    message = 'Only instructors and admins can perform this action.'

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role in (user.Role.ADMIN, user.Role.INSTRUCTOR)
        )


class IsAdmin(BasePermission):
    message = 'Only admins can perform this action.'

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == user.Role.ADMIN)


class IsOwnerOrInstructorOrAdmin(BasePermission):
    message = 'You do not have permission to access this object.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == user.Role.ADMIN:
            return True
        if user.role == user.Role.INSTRUCTOR:
            return obj.instructor == user or obj.course.instructor == user
        return obj.student == user