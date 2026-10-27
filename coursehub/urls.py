from django.urls import path

from . import views

urlpatterns = [
    path("faculties/", views.FacultyListView.as_view(), name="faculty-list"),
    path(
        "faculties/<int:pk>/", views.FacultyDetailView.as_view(), name="faculty-detail"
    ),
    path("teachers/", views.TeacherListView.as_view(), name="teacher-list"),
    path(
        "teachers/<int:pk>/", views.TeacherDetailView.as_view(), name="teacher-detail"
    ),
    path("courses/", views.CourseListView.as_view(), name="course-list"),
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="course-detail"),
]
