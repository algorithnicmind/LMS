from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LessonCompletionViewSet, CourseProgressViewSet, InstructorReportViewSet, AdminReportViewSet

router = DefaultRouter()
router.register(r'lesson-completions', LessonCompletionViewSet, basename='lesson-completion')
router.register(r'course-progress', CourseProgressViewSet, basename='course-progress')
router.register(r'instructor/reports', InstructorReportViewSet, basename='instructor-report')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/reports/', AdminReportViewSet.as_view({'get': 'list'}), name='admin-reports'),
]