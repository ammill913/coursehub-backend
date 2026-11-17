import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from coursehub.models import Course, Faculty, Teacher

PASSWORD = "StrongPass123!"


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username="student", email="student@example.com", password=PASSWORD
    )


@pytest.fixture
def staff_user() -> User:
    return User.objects.create_user(
        username="manager",
        email="manager@example.com",
        password=PASSWORD,
        is_staff=True,
    )


def make_client(username: str) -> APIClient:
    client = APIClient()
    response = client.post(
        reverse("login"), {"username": username, "password": PASSWORD}, format="json"
    )
    client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])
    return client


@pytest.fixture
def user_client(user) -> APIClient:
    return make_client(user.username)


@pytest.fixture
def staff_client(staff_user) -> APIClient:
    return make_client(staff_user.username)


@pytest.fixture
def faculty() -> Faculty:
    return Faculty.objects.create(name="ФСНСТ", description="Соціальні науки")


@pytest.fixture
def teacher(faculty) -> Teacher:
    return Teacher.objects.create(
        first_name="Максим",
        last_name="Яковлєв",
        position="associate_professor",
        faculty=faculty,
    )


@pytest.fixture
def course(faculty, teacher) -> Course:
    return Course.objects.create(
        title="Вступ до аналітики",
        description="Базовий курс",
        credits=4,
        faculty=faculty,
        teacher=teacher,
    )


@pytest.fixture
def course_data(faculty, teacher) -> dict:
    return {
        "title": "Міжнародна безпека",
        "description": "Новий курс",
        "credits": 4.5,
        "faculty": faculty.id,
        "teacher": teacher.id,
    }
