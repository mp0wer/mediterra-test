# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from rest_framework import serializers
from .models import Teacher, Student, Grade, Specialization


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentSerializer, self).__init__(*args, **kwargs)
        self.partial = True


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def validate(self, attrs):
        instance = Grade(**attrs)
        instance.clean()
        return attrs


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'
