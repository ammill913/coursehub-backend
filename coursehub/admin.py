from django.contrib import admin

from .models import Course, Faculty, Teacher

admin.site.register(Faculty)
admin.site.register(Teacher)
admin.site.register(Course)
