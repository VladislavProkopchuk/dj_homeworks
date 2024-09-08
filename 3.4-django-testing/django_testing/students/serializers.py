from django.conf import settings
from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        method = self.context["request"].method
        if method in ['POST', 'PUT', 'PATCH']:
            # смотрим сколько студентов хотят записать на курс
            students = self.context["request"].data.get('students', [])
            students_per_course = len(students)
            if students_per_course > settings.MAX_STUDENTS_PER_COURSE:
                message = 'Course can only have not great %d students.' % settings.MAX_STUDENTS_PER_COURSE
                raise serializers.ValidationError(message)

        return data
