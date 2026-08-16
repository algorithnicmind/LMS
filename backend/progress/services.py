from django.db.models import Count

from .models import CourseProgress
from courses.models import Lesson


def recompute_course_progress(student, course):
    """Recalculate and update course progress for a student."""
    total_lessons = Lesson.objects.filter(course=course).count()
    completed_lessons = CourseProgress.objects.filter(
        student=student,
        lesson__course=course,
    ).count()

    percent = 0
    if total_lessons > 0:
        percent = round((completed_lessons / total_lessons) * 100, 2)

    CourseProgress.objects.update_or_create(
        student=student,
        course=course,
        defaults={
            'completed_lessons': completed_lessons,
            'total_lessons': total_lessons,
            'percent': percent,
        }
    )

    return percent


def recompute_all_student_progress(student):
    """Recompute progress for all courses a student is enrolled in."""
    from courses.models import Enrollment
    enrollments = Enrollment.objects.filter(student=student, status=Enrollment.Status.ACTIVE)
    for enrollment in enrollments:
        recompute_course_progress(student, enrollment.course)