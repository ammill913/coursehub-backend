import logging

from django.db.models import ProtectedError
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Faculty, Teacher
from .serializers import CourseSerializer, FacultySerializer, TeacherSerializer

logger = logging.getLogger(__name__)


class CatalogDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]


class FacultyListView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request):
        faculties = Faculty.objects.all()
        logger.debug("Отримано список факультетів (кількість=%s)", faculties.count())
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FacultySerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "Помилка валідації при створенні факультету (user=%s): %s",
                request.user.username,
                list(serializer.errors.keys()),
            )
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        faculty = serializer.save()
        logger.info(
            "Створено факультет id=%s '%s' (user=%s)",
            faculty.id,
            faculty.name,
            request.user.username,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FacultyDetailView(CatalogDetailView):
    def get_object(self, pk):
        try:
            return Faculty.objects.get(pk=pk)
        except Faculty.DoesNotExist:
            return None

    def get(self, request, pk):
        faculty = self.get_object(pk)
        if not faculty:
            logger.warning("Запит неіснуючого факультету id=%s", pk)
            return Response(
                {"error": "Факультет з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = FacultySerializer(faculty)
        return Response(serializer.data)

    def put(self, request, pk):
        faculty = self.get_object(pk)
        if not faculty:
            logger.warning(
                "Спроба оновити неіснуючий факультет id=%s (user=%s)",
                pk,
                request.user.username,
            )
            return Response(
                {"error": "Факультет з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = FacultySerializer(faculty, data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "Помилка валідації при оновленні факультету id=%s (user=%s): %s",
                pk,
                request.user.username,
                list(serializer.errors.keys()),
            )
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        logger.info("Оновлено факультет id=%s (user=%s)", pk, request.user.username)
        return Response(serializer.data)

    def delete(self, request, pk):
        faculty = self.get_object(pk)
        if not faculty:
            logger.warning(
                "Спроба видалити неіснуючий факультет id=%s (user=%s)",
                pk,
                request.user.username,
            )
            return Response(
                {"error": "Факультет з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            faculty.delete()
        except ProtectedError as e:
            protected_count = len(e.protected_objects)
            logger.warning(
                "Конфлікт при видаленні факультету id=%s: прив'язано %s об'єкт(ів) (user=%s)",
                pk,
                protected_count,
                request.user.username,
            )
            return Response(
                {
                    "error": f"Неможливо видалити факультет, оскільки до нього прив'язано {protected_count} об'єкт(ів) (викладачів або курсів)."
                },
                status=status.HTTP_409_CONFLICT,
            )

        logger.info("Видалено факультет id=%s (user=%s)", pk, request.user.username)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherListView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request):
        teachers = Teacher.objects.all()
        logger.debug("Отримано список викладачів (кількість=%s)", teachers.count())
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "Помилка валідації при створенні викладача (user=%s): %s",
                request.user.username,
                list(serializer.errors.keys()),
            )
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        teacher = serializer.save()
        logger.info(
            "Створено викладача id=%s (user=%s)", teacher.id, request.user.username
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeacherDetailView(CatalogDetailView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return None

    def get(self, request, pk):
        teacher = self.get_object(pk)
        if not teacher:
            logger.warning("Запит неіснуючого викладача id=%s", pk)
            return Response(
                {"error": "Викладача з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, pk):
        teacher = self.get_object(pk)
        if not teacher:
            logger.warning(
                "Спроба оновити неіснуючого викладача id=%s (user=%s)",
                pk,
                request.user.username,
            )
            return Response(
                {"error": "Викладача з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TeacherSerializer(teacher, data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "Помилка валідації при оновленні викладача id=%s (user=%s): %s",
                pk,
                request.user.username,
                list(serializer.errors.keys()),
            )
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        logger.info("Оновлено викладача id=%s (user=%s)", pk, request.user.username)
        return Response(serializer.data)

    def delete(self, request, pk):
        teacher = self.get_object(pk)
        if not teacher:
            logger.warning(
                "Спроба видалити неіснуючого викладача id=%s (user=%s)",
                pk,
                request.user.username,
            )
            return Response(
                {"error": "Викладача з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            teacher.delete()
        except ProtectedError as e:
            protected_count = len(e.protected_objects)
            logger.warning(
                "Конфлікт при видаленні викладача id=%s: закріплено %s курс(ів) (user=%s)",
                pk,
                protected_count,
                request.user.username,
            )
            return Response(
                {
                    "error": f"Неможливо видалити викладача, оскільки за ним закріплено {protected_count} курс(ів)."
                },
                status=status.HTTP_409_CONFLICT,
            )

        logger.info("Видалено викладача id=%s (user=%s)", pk, request.user.username)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseListView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]

    @extend_schema(
        summary="Отримати список усіх курсів",
        description="Доступно всім користувачам (включно з неавторизованими).",
        responses={200: CourseSerializer(many=True)},
    )
    def get(self, request):
        courses = Course.objects.all()
        logger.debug("Отримано список курсів (кількість=%s)", courses.count())
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Створити новий курс",
        description="Доступно лише авторизованим користувачам (потрібен JWT access-токен).",
        request=CourseSerializer,
        responses={
            201: CourseSerializer,
            400: OpenApiResponse(description="Невалідні дані запиту"),
            401: OpenApiResponse(description="Користувач не авторизований"),
        },
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "Помилка валідації при створенні курсу (user=%s): %s",
                request.user.username,
                list(serializer.errors.keys()),
            )
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course = serializer.save()
        logger.info(
            "Створено курс id=%s '%s' (user=%s)",
            course.id,
            course.title,
            request.user.username,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseDetailView(CatalogDetailView):
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    @extend_schema(
        summary="Отримати деталі курсу за ID",
        description="Доступно всім користувачам.",
        responses={
            200: CourseSerializer,
            404: OpenApiResponse(description="Курс з таким ID не знайдено"),
        },
    )
    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            logger.warning("Запит неіснуючого курсу id=%s", pk)
            return Response(
                {"error": "Курс з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @extend_schema(
        summary="Повністю оновити курс",
        description="Доступно авторизованим користувачам.",
        request=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: OpenApiResponse(description="Невалідні дані запиту"),
            401: OpenApiResponse(description="Користувач не авторизований"),
            404: OpenApiResponse(description="Курс з таким ID не знайдено"),
        },
    )
    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            logger.warning(
                "Спроба оновити неіснуючий курс id=%s (user=%s)",
                pk,
                request.user.username,
            )
            return Response(
                {"error": "Курс з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CourseSerializer(course, data=request.data)
        if not serializer.is_valid():
            logger.warning(
                "Помилка валідації при оновленні курсу id=%s (user=%s): %s",
                pk,
                request.user.username,
                list(serializer.errors.keys()),
            )
            return Response(
                {"error": "Передані невалідні дані.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        logger.info("Оновлено курс id=%s (user=%s)", pk, request.user.username)
        return Response(serializer.data)

    @extend_schema(
        summary="Видалити курс",
        description="Доступно лише адміністраторам (`is_staff=True`).",
        responses={
            204: OpenApiResponse(description="Курс успішно видалено"),
            401: OpenApiResponse(description="Користувач не авторизований"),
            403: OpenApiResponse(
                description="Недостатньо прав (потрібні права адміністратора)"
            ),
            404: OpenApiResponse(description="Курс з таким ID не знайдено"),
        },
    )
    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            logger.warning(
                "Спроба видалити неіснуючий курс id=%s (user=%s)",
                pk,
                request.user.username,
            )
            return Response(
                {"error": "Курс з таким ID не знайдено."},
                status=status.HTTP_404_NOT_FOUND,
            )

        course.delete()
        logger.info("Видалено курс id=%s (user=%s)", pk, request.user.username)
        return Response(status=status.HTTP_204_NO_CONTENT)
