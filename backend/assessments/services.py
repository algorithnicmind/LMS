from decimal import Decimal
from django.utils import timezone

from .models import QuizAttempt, Submission


def grade_quiz(attempt: QuizAttempt, answers: dict) -> Decimal:
    """Auto-grade a quiz attempt."""
    quiz = attempt.quiz
    total_questions = quiz.questions.count()

    if total_questions == 0:
        return Decimal('0.00')

    correct_count = 0
    for question in quiz.questions.all():
        given_option_id = answers.get(str(question.id))
        if given_option_id:
            try:
                option = Option.objects.get(id=given_option_id, question=question)
                if option.is_correct:
                    correct_count += 1
            except Option.DoesNotExist:
                pass

    score = (Decimal(correct_count) / Decimal(total_questions)) * Decimal('100')
    return score.quantize(Decimal('0.01'))


def grade_assignment(submission: Submission, grade: Decimal, feedback: str = '') -> None:
    """Grade an assignment submission."""
    from .models import Assignment
    assignment = submission.assignment

    if grade > assignment.max_points:
        raise ValueError('Grade cannot exceed max points')

    submission.grade = grade
    submission.feedback = feedback
    submission.graded_at = timezone.now()
    submission.save(update_fields=['grade', 'feedback', 'graded_at'])