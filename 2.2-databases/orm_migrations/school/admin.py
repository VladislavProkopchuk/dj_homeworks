from django.contrib import admin

from .models import Student, Teacher, TeacherStudent


class TeacherStudentInline(admin.TabularInline):
    model = TeacherStudent
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [TeacherStudentInline, ]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass
