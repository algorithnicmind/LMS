from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Quiz(models.Model):
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='quizzes',
    )
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    time_limit_minutes = models.PositiveIntegerField(_('time limit (minutes)'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('quiz')
        verbose_name_plural = _('quizzes')
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
    )
    text = models.TextField(_('question text'))
    order = models.PositiveIntegerField(_('order'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        ordering = ['quiz', 'order']

    def __str__(self):
        return f'{self.quiz.title} - Q{self.order}'


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options',
    )
    text = models.CharField(_('option text'), max_length=255)
    is_correct = models.BooleanField(_('is correct'), default=False)
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('option')
        verbose_name_plural = _('options')
        ordering = ['question', 'order']

    def __str__(self):
        return f'{self.question} - {self.text[:50]}'


class QuizAttempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        limit_choices_to={'role': 'STUDENT'},
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts',
    )
    score = models.DecimalField(_('score'), max_digits=5, decimal_places=2, default=0)
    answers = models.JSONField(_('answers'), default=dict)  # {question_id: option_id}
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('quiz attempt')
        verbose_name_plural = _('quiz attempts')
        ordering = ['-submitted_at']
        constraints = [
            models.UniqueConstraint(fields=['student', 'quiz'], name='unique_quiz_attempt_per_student'),
        ]

    def __str__(self):
        return f'{self.student.name} - {self.quiz.title}: {self.score}%'


class Assignment(models.Model):
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    due_date = models.DateTimeField(_('due date'))
    max_points = models.PositiveIntegerField(_('max points'), default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')
        ordering = ['-due_date']

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions',
        limit_choices_to={'role': 'STUDENT'},
    )
    content = models.TextField(_('content'), blank=True)
    file = models.FileField(_('file'), upload_to='submissions/', blank=True, null=True)
    grade = models.DecimalField(_('grade'), max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(_('feedback'), blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('submission')
        verbose_name_plural = _('submissions')
        ordering = ['-submitted_at']
        constraints = [
            models.UniqueConstraint(fields=['assignment', 'student'], name='unique_submission_per_assignment_student'),
        ]

    def __str__(self):
        return f'{self.student.name} - {self.assignment.title}'