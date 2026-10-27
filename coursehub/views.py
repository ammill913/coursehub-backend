from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Faculty, Teacher
from .serializers import CourseSerializer, FacultySerializer, TeacherSerializer


class FacultyListView(APIView):
    def get(self, request):
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FacultySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FacultyDetailView(APIView):
    def get_object(self, pk):
        try:
            return Faculty.objects.get(pk=pk)
        except Faculty.DoesNotExist:
            return None

    def get(self, request, pk):
        faculty = self.get_object(pk)
        if not faculty:
            return Response(
                {"error": "Факультет з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = FacultySerializer(faculty)
        return Response(serializer.data)

    def put(self, request, pk):
        faculty = self.get_object(pk)
        if not faculty:
            return Response(
                {"error": "Факультет з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = FacultySerializer(faculty, data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        faculty = self.get_object(pk)
        if not faculty:
            return Response(
                {"error": "Факультет з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            faculty.delete()
        except ProtectedError as e:
            protected_count = len(e.protected_objects)
            return Response(
                {
                    "error": f"Неможливо видалити факультет, оскільки до нього прив'язано {protected_count} об'єкт(ів) (викладачів або курсів)."
                },
                status=status.HTTP_409_CONFLICT,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherListView(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeacherDetailView(APIView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return None

    def get(self, request, pk):
        teacher = self.get_object(pk)
        if not teacher:
            return Response(
                {"error": "Викладача з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, pk):
        teacher = self.get_object(pk)
        if not teacher:
            return Response(
                {"error": "Викладача з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TeacherSerializer(teacher, data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        teacher = self.get_object(pk)
        if not teacher:
            return Response(
                {"error": "Викладача з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            teacher.delete()
        except ProtectedError as e:
            protected_count = len(e.protected_objects)
            return Response(
                {
                    "error": f"Неможливо видалити викладача, оскільки за ним закріплено {protected_count} курс(ів)."
                },
                status=status.HTTP_409_CONFLICT,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseListView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseDetailView(APIView):
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(
                {"error": "Курс з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(
                {"error": "Курс з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CourseSerializer(course, data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(
                {"error": "Курс з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
