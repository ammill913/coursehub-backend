from rest_framework import serializers

from .models import Course, Faculty, Teacher


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "position", "email", "faculty"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "credits", "faculty", "teacher"]

    def validate_credits(self, value):
        if (value * 2) % 1 != 0:
            raise serializers.ValidationError("Кількість кредитів має бути кратною 0.5")
        return value
