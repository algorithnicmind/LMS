from rest_framework import serializers
from .models import Quiz, Question, Option, QuizAttempt, Assignment, Submission


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'order']
        # is_correct hidden from students


class OptionInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'order', 'options']


class QuestionInstructorSerializer(serializers.ModelSerializer):
    options = OptionInstructorSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'order', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question


class QuizListSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'time_limit_minutes', 'course', 'course_title', 'questions_count', 'created_at']

    def get_questions_count(self, obj):
        return obj.questions.count()


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'time_limit_minutes', 'course', 'course_title', 'questions', 'created_at']


class QuizInstructorSerializer(serializers.ModelSerializer):
    questions = QuestionInstructorSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'time_limit_minutes', 'course', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)
        for q_data in questions_data:
            options_data = q_data.pop('options')
            question = Question.objects.create(quiz=quiz, **q_data)
            for opt_data in options_data:
                Option.objects.create(question=question, **opt_data)
        return quiz


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'score', 'answers', 'submitted_at']
        read_only_fields = ['id', 'score', 'submitted_at']


class QuizAttemptSubmitSerializer(serializers.Serializer):
    answers = serializers.DictField(
        child=serializers.IntegerField(),
        help_text='Mapping of question_id to option_id'
    )


class AssignmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'max_points', 'course', 'course_title', 'created_at']


class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'student_name', 'content', 'file', 'grade', 'feedback', 'submitted_at', 'graded_at']
        read_only_fields = ['id', 'student', 'submitted_at', 'graded_at', 'grade', 'feedback']


class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['content', 'file']


class SubmissionGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['grade', 'feedback']