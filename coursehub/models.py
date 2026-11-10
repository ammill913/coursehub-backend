from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Teacher(models.Model):
    class Position(models.TextChoices):
        PROFESSOR = "professor", "професор"
        ASSOCIATE_PROFESSOR = "associate_professor", "доцент"
        SENIOR_LECTURER = "senior_lecturer", "старший викладач"
        ASSISTANT = "assistant", "асистент"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=30, choices=Position.choices)
    email = models.EmailField(blank=True)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.PROTECT, related_name="teachers"
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.position})"


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    faculty = models.ForeignKey(
        Faculty, related_name="courses", on_delete=models.PROTECT
    )
    teacher = models.ForeignKey(
        Teacher, related_name="courses", on_delete=models.PROTECT
    )
    credits = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(15)],
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
