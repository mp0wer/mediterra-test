# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import django_filters
from .models import Teacher, Student, Grade


class TeacherFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Student
        fields = '__all__'


class GradeFilter(django_filters.rest_framework.FilterSet):
    teacher = django_filters.ModelMultipleChoiceFilter(queryset=Teacher.objects.all())

    class Meta:
        model = Grade
        fields = '__all__'
