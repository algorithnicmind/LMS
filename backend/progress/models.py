from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class LessonCompletion(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_completions',
        limit_choices_to={'role': 'STUDENT'},
    )
    lesson = models.ForeignKey(
        'courses.Lesson',
        on_delete=models.CASCADE,
        related_name='completions',
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('lesson completion')
        verbose_name_plural = _('lesson completions')
        ordering = ['-completed_at']
        constraints = [
            models.UniqueConstraint(fields=['student', 'lesson'], name='unique_lesson_completion_per_student'),
        ]

    def __str__(self):
        return f'{self.student.name} - {self.lesson.title}'


class CourseProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_progress',
        limit_choices_to={'role': 'STUDENT'},
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='progress_records',
    )
    completed_lessons = models.PositiveIntegerField(_('completed lessons'), default=0)
    total_lessons = models.PositiveIntegerField(_('total lessons'), default=0)
    percent = models.DecimalField(_('percent'), max_digits=5, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('course progress')
        verbose_name_plural = _('course progress records')
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_course_progress_per_student'),
        ]

    def __str__(self):
        return f'{self.student.name} - {self.course.title}: {self.percent}%'