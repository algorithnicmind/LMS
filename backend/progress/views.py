from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import LessonCompletion, CourseProgress
from .serializers import (
    LessonCompletionSerializer,
    CourseProgressSerializer,
    InstructorStudentProgressSerializer,
    AdminPlatformStatsSerializer,
)
from users.permissions import IsInstructorOrAdmin
from .services import recompute_course_progress


class LessonCompletionViewSet(viewsets.ModelViewSet):
    serializer_class = LessonCompletionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['lesson', 'lesson__course']
    ordering_fields = ['completed_at']
    ordering = ['-completed_at']

    def get_queryset(self):
        return LessonCompletion.objects.filter(student=self.request.user).select_related('lesson', 'lesson__course')

    def create(self, request, *args, **kwargs):
        lesson_id = request.data.get('lesson')
        if not lesson_id:
            return Response(
                {'error': {'code': 'lesson_required', 'message': 'Lesson ID is required'}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        completion, created = LessonCompletion.objects.get_or_create(
            student=request.user,
            lesson_id=lesson_id,
        )

        if created:
            recompute_course_progress(request.user, completion.lesson.course)

        return Response(self.get_serializer(completion).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class CourseProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseProgressSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course']
    ordering_fields = ['updated_at', 'percent']
    ordering = ['-updated_at']

    def get_queryset(self):
        return CourseProgress.objects.filter(student=self.request.user).select_related('course')

    @action(detail=False, methods=['get'])
    def summary(self, request):
        progress = self.get_queryset()
        total = progress.count()
        completed = progress.filter(percent=100).count()
        in_progress = total - completed
        avg_percent = progress.aggregate(avg=models.Avg('percent'))['avg'] or 0

        return Response({
            'total_courses': total,
            'completed': completed,
            'in_progress': in_progress,
            'average_progress': round(avg_percent, 2),
        })


class InstructorReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InstructorStudentProgressSerializer
    permission_classes = [IsAuthenticated, IsInstructorOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'student']
    ordering_fields = ['updated_at', 'percent']
    ordering = ['-updated_at']

    def get_queryset(self):
        return CourseProgress.objects.filter(
            course__instructor=self.request.user
        ).select_related('student', 'course')


class AdminReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        from users.models import CustomUser
        from courses.models import Course, Enrollment
        from django.db.models import Avg, Count

        if request.user.role != request.user.Role.ADMIN:
            return Response(
                {'error': {'code': 'permission_denied', 'message': 'Admin access required'}},
                status=403,
            )

        total_users = CustomUser.objects.count()
        total_students = CustomUser.objects.filter(role=CustomUser.Role.STUDENT).count()
        total_instructors = CustomUser.objects.filter(role=CustomUser.Role.INSTRUCTOR).count()
        total_courses = Course.objects.count()
        total_enrollments = Enrollment.objects.filter(status=Enrollment.Status.ACTIVE).count()

        avg_completion = CourseProgress.objects.aggregate(avg=Avg('percent'))['avg'] or 0

        serializer = AdminPlatformStatsSerializer({
            'total_users': total_users,
            'total_students': total_students,
            'total_instructors': total_instructors,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'avg_completion_rate': round(avg_completion, 2),
        })
        return Response(serializer.data)