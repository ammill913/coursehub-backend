import pytest
from django.urls import reverse
from coursehub.models import Course

@pytest.mark.django_db
def test_list_courses_without_login(api_client, course) -> None:
    response = api_client.get(reverse("course-list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Вступ до аналітики"

@pytest.mark.django_db
def test_list_courses_empty(api_client) -> None:
    response = api_client.get(reverse("course-list"))
    assert response.status_code == 200
    assert response.data == []

@pytest.mark.django_db
def test_get_course(api_client, course) -> None:
    response = api_client.get(reverse("course-detail", args=[course.id]))
    assert response.status_code == 200
    assert response.data["id"] == course.id
    assert response.data["credits"] == "4.0"

@pytest.mark.django_db
def test_get_missing_course(api_client) -> None:
    response = api_client.get(reverse("course-detail", args=[999]))
    assert response.status_code == 404
    assert "error" in response.data

@pytest.mark.django_db
def test_admin_creates_course(staff_client, course_data) -> None:
    response = staff_client.post(reverse("course-list"), course_data, format="json")
    assert response.status_code == 201
    assert response.data["title"] == "Міжнародна безпека"
    assert Course.objects.filter(title="Міжнародна безпека").exists()

@pytest.mark.django_db
def test_user_creates_course(user_client, course_data) -> None:
    response = user_client.post(reverse("course-list"), course_data, format="json")
    assert response.status_code == 201
    assert response.data["title"] == "Міжнародна безпека"
    assert Course.objects.filter(title="Міжнародна безпека").exists()

@pytest.mark.django_db
def test_create_course_without_login(api_client, course_data) -> None:
    response = api_client.post(reverse("course-list"), course_data, format="json")
    assert response.status_code == 401
    assert Course.objects.count() == 0

@pytest.mark.django_db
def test_create_course_with_invalid_token(api_client, course_data) -> None:
    api_client.credentials(HTTP_AUTHORIZATION="Bearer not-a-real-token")
    response = api_client.post(reverse("course-list"), course_data, format="json")
    assert response.status_code == 401

@pytest.mark.django_db
def test_create_course_without_title(staff_client, course_data) -> None:
    del course_data["title"]
    response = staff_client.post(reverse("course-list"), course_data, format="json")
    assert response.status_code == 400
    assert "title" in response.data["details"]

@pytest.mark.django_db
def test_create_course_with_credits_not_multiple_of_half(staff_client, course_data) -> None:
    course_data["credits"] = 2.3
    response = staff_client.post(reverse("course-list"), course_data, format="json")
    assert response.status_code == 400
    assert "credits" in response.data["details"]

@pytest.mark.django_db
def test_create_course_with_too_many_credits(staff_client, course_data) -> None:
    course_data["credits"] = 20
    response = staff_client.post(reverse("course-list"), course_data, format="json")
    assert response.status_code == 400
    assert "credits" in response.data["details"]

@pytest.mark.django_db
def test_create_course_with_unknown_faculty(staff_client, course_data) -> None:
    course_data["faculty"] = 999
    response = staff_client.post(reverse("course-list"), course_data, format="json")
    assert response.status_code == 400
    assert "faculty" in response.data["details"]

@pytest.mark.django_db
def test_create_course_with_broken_json(staff_client) -> None:
    response = staff_client.post(reverse("course-list"), "{bad json", content_type="application/json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_admin_updates_course(staff_client, course, course_data) -> None:
    course_data["title"] = "Нова назва"
    response = staff_client.put(reverse("course-detail", args=[course.id]), course_data, format="json")
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.title == "Нова назва"

@pytest.mark.django_db
def test_user_updates_course(user_client, course, course_data) -> None:
    course_data["title"] = "Оновлена назва користувачем"
    response = user_client.put(reverse("course-detail", args=[course.id]), course_data, format="json")
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.title == "Оновлена назва користувачем"

@pytest.mark.django_db
def test_update_course_without_login(api_client, course, course_data) -> None:
    response = api_client.put(reverse("course-detail", args=[course.id]), course_data, format="json")
    assert response.status_code == 401

@pytest.mark.django_db
def test_update_missing_course(staff_client, course_data) -> None:
    response = staff_client.put(reverse("course-detail", args=[999]), course_data, format="json")
    assert response.status_code == 404

@pytest.mark.django_db
def test_update_course_with_invalid_data(staff_client, course, course_data) -> None:
    course_data["credits"] = 0
    response = staff_client.put(reverse("course-detail", args=[course.id]), course_data, format="json")
    assert response.status_code == 400
    assert "credits" in response.data["details"]

@pytest.mark.django_db
def test_patch_is_not_supported(staff_client, course) -> None:
    response = staff_client.patch(reverse("course-detail", args=[course.id]), {"title": "x"}, format="json")
    assert response.status_code == 405

@pytest.mark.django_db
def test_admin_deletes_course(staff_client, course) -> None:
    response = staff_client.delete(reverse("course-detail", args=[course.id]))
    assert response.status_code == 204
    assert Course.objects.count() == 0

@pytest.mark.django_db
def test_user_cannot_delete_course(user_client, course) -> None:
    response = user_client.delete(reverse("course-detail", args=[course.id]))
    assert response.status_code == 403
    assert Course.objects.count() == 1

@pytest.mark.django_db
def test_delete_course_without_login(api_client, course) -> None:
    response = api_client.delete(reverse("course-detail", args=[course.id]))
    assert response.status_code == 401
    assert Course.objects.count() == 1

@pytest.mark.django_db
def test_delete_missing_course(staff_client) -> None:
    response = staff_client.delete(reverse("course-detail", args=[999]))
    assert response.status_code == 404