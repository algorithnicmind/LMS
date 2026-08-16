from rest_framework import serializers
from .models import LessonCompletion, CourseProgress
from courses.serializers import LessonSerializer
from courses.models import Course


class LessonCompletionSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = LessonCompletion
        fields = ['id', 'lesson', 'lesson_title', 'completed_at']
        read_only_fields = ['id', 'completed_at']


class CourseProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_thumbnail = serializers.ImageField(source='course.thumbnail', read_only=True)

    class Meta:
        model = CourseProgress
        fields = ['id', 'course', 'course_title', 'course_thumbnail', 'completed_lessons', 'total_lessons', 'percent', 'updated_at']
        read_only_fields = ['id', 'completed_lessons', 'total_lessons', 'percent', 'updated_at']


class StudentProgressSerializer(serializers.ModelSerializer):
    course = CourseProgressSerializer(read_only=True)

    class Meta:
        model = CourseProgress
        fields = ['course']


class InstructorStudentProgressSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseProgress
        fields = ['id', 'student', 'student_name', 'student_email', 'course', 'course_title', 'completed_lessons', 'total_lessons', 'percent', 'updated_at']


class AdminPlatformStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_students = serializers.IntegerField()
    total_instructors = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    total_enrollments = serializers.IntegerField()
    avg_completion_rate = serializers.DecimalField(max_digits=5, decimal_places=2)