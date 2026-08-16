from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Quiz, Question, Option, QuizAttempt, Assignment, Submission
from .serializers import (
    QuizListSerializer,
    QuizDetailSerializer,
    QuizInstructorSerializer,
    QuizAttemptSerializer,
    QuizAttemptSubmitSerializer,
    AssignmentSerializer,
    SubmissionSerializer,
    SubmissionCreateSerializer,
    SubmissionGradeSerializer,
)
from users.permissions import IsInstructorOrAdmin, IsOwnerOrInstructorOrAdmin
from .services import grade_quiz, grade_assignment


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.select_related('course').prefetch_related('questions__options')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course']
    search_fields = ['title']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return QuizInstructorSerializer
        return QuizListSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsInstructorOrAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.role == self.request.user.Role.STUDENT:
            return qs.filter(course__enrollments__student=self.request.user, course__enrollments__status='ACTIVE')
        return qs

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='attempt')
    def attempt(self, request, pk=None):
        quiz = self.get_object()
        serializer = QuizAttemptSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attempt, created = QuizAttempt.objects.get_or_create(
            student=request.user,
            quiz=quiz,
            defaults={'answers': serializer.validated_data['answers']},
        )

        if not created:
            return Response(
                {'error': {'code': 'already_attempted', 'message': 'Quiz already attempted'}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        score = grade_quiz(attempt, serializer.validated_data['answers'])
        attempt.score = score
        attempt.save()

        return Response(QuizAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('course')
    serializer_class = AssignmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course']
    search_fields = ['title']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['-due_date']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsInstructorOrAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.role == self.request.user.Role.STUDENT:
            return qs.filter(course__enrollments__student=self.request.user, course__enrollments__status='ACTIVE')
        return qs

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='submit')
    def submit(self, request, pk=None):
        assignment = self.get_object()
        serializer = SubmissionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission, created = Submission.objects.get_or_create(
            assignment=assignment,
            student=request.user,
            defaults=serializer.validated_data,
        )

        if not created:
            return Response(
                {'error': {'code': 'already_submitted', 'message': 'Assignment already submitted'}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related('assignment', 'student')
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrInstructorOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['assignment']
    ordering_fields = ['submitted_at']
    ordering = ['-submitted_at']

    def get_queryset(self):
        user = self.request.user
        if user.role == user.Role.ADMIN:
            return super().get_queryset()
        if user.role == user.Role.INSTRUCTOR:
            return super().get_queryset().filter(assignment__course__instructor=user)
        return super().get_queryset().filter(student=user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='grade')
    def grade(self, request, pk=None):
        submission = self.get_object()
        if not request.user.role in (request.user.Role.INSTRUCTOR, request.user.Role.ADMIN):
            if submission.assignment.course.instructor != request.user:
                return Response(
                    {'error': {'code': 'permission_denied', 'message': 'Not authorized to grade'}},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = SubmissionGradeSerializer(submission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()
        grade_assignment(submission, serializer.validated_data['grade'], serializer.validated_data.get('feedback', ''))
        return Response(SubmissionSerializer(submission).data)