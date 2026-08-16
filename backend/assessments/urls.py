from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import QuizViewSet, AssignmentViewSet, SubmissionViewSet

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'submissions', SubmissionViewSet, basename='submission')

urlpatterns = [
    path('', include(router.urls)),
]