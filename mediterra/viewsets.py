# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from rest_framework import viewsets
from .models import Teacher, Student, Specialization, Grade
from .serializers import TeacherSerializer, StudentSerializer, GradeSerializer, SpecializationSerializer
from .filters import TeacherFilter, StudentFilter, GradeFilter


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_class = TeacherFilter


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_class = StudentFilter


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filter_class = GradeFilter


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
