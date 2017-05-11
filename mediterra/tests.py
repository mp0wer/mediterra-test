# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Teacher, Student, Grade, Specialization


class TeacherAPITestCase(APITestCase):
    list_url_name = 'teacher-list'
    detail_url_name = 'teacher-detail'
    test_data = {
        'first_name': 'Иван',
        'last_name': 'Иванов'
    }

    def setUp(self):
        super(TeacherAPITestCase, self).setUp()
        self.specialization1 = Specialization.objects.create(title='Английский язык')
        self.specialization2 = Specialization.objects.create(title='Математика')

    def createTeacher(self):
        teacher = Teacher.objects.create(**self.test_data)
        teacher.specializations.add(self.specialization1)
        return teacher

    def test_get_list(self):
        response = self.client.get(reverse(self.list_url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        self.createTeacher()
        response = self.client.get(reverse(self.list_url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_last_name(self):
        self.createTeacher()
        response = self.client.get(reverse(self.list_url_name), {'last_name': self.test_data['last_name']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response = self.client.get(reverse(self.list_url_name), {'last_name': 'Неизвестный'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create(self):
        response = self.client.post(reverse(self.list_url_name),
                                    dict(self.test_data, specializations=[self.specialization1.pk]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.all().count(), 1)

    def test_get(self):
        teacher = self.createTeacher()
        response = self.client.get(reverse(self.detail_url_name, kwargs={'pk': teacher.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], teacher.pk)

    def test_delete(self):
        teacher = self.createTeacher()
        response = self.client.delete(reverse(self.detail_url_name, kwargs={'pk': teacher.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Teacher.objects.count(), 0)

    def test_update(self):
        teacher = self.createTeacher()
        update_data = {
            'first_name': 'Сергей',
            'last_name': 'Сидоров',
            'specializations': [self.specialization2.pk]
        }
        response = self.client.put(reverse(self.detail_url_name, kwargs={'pk': teacher.pk}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        teacher = Teacher.objects.get(pk=teacher.pk)
        self.assertEqual(teacher.first_name, update_data['first_name'])
        self.assertEqual(teacher.last_name, update_data['last_name'])
        self.assertEqual(list(teacher.specializations.all()), [self.specialization2])


class StudentAPITestCase(APITestCase):
    list_url_name = 'student-list'
    detail_url_name = 'student-detail'
    test_data = {
        'first_name': 'Петр',
        'last_name': 'Петров'
    }

    def setUp(self):
        super(StudentAPITestCase, self).setUp()
        self.specialization = Specialization.objects.create(title='Английский язык')
        self.teacher = Teacher.objects.create(**self.test_data)
        self.teacher.specializations.add(self.specialization)
        self.grade1 = Grade.objects.create(title='5a', specialization=self.specialization, teacher=self.teacher)
        self.grade2 = Grade.objects.create(title='5б', specialization=self.specialization, teacher=self.teacher)

    def test_get_list(self):
        response = self.client.get(reverse(self.list_url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        Student.objects.create(**self.test_data)
        response = self.client.get(reverse(self.list_url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_last_name(self):
        Student.objects.create(**self.test_data)
        response = self.client.get(reverse(self.list_url_name), {'last_name': self.test_data['last_name']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response = self.client.get(reverse(self.list_url_name), {'last_name': 'Неизвестный'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_filter_by_grade(self):
        student1 = Student.objects.create(**self.test_data)
        response = self.client.get(reverse(self.list_url_name), {'grades': self.grade1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        student1.grades.add(self.grade1)
        student2 = Student.objects.create(first_name='Павел', last_name='Павлов')
        student2.grades.add(self.grade2)
        response = self.client.get(reverse(self.list_url_name), {'grades': self.grade1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response = self.client.get(reverse(self.list_url_name), {'grades': [self.grade1.pk, self.grade2.pk]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        response = self.client.post(reverse(self.list_url_name), self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.all().count(), 1)

    def test_get(self):
        student = Student.objects.create(**self.test_data)
        response = self.client.get(reverse(self.detail_url_name, kwargs={'pk': student.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], student.pk)

    def test_delete(self):
        student = Student.objects.create(**self.test_data)
        response = self.client.delete(reverse(self.detail_url_name, kwargs={'pk': student.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)

    def test_update(self):
        student = Student.objects.create(**self.test_data)
        update_data = {
            'first_name': 'Сергей',
            'last_name': 'Сидоров'
        }
        response = self.client.put(reverse(self.detail_url_name, kwargs={'pk': student.pk}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student = Student.objects.get(pk=student.pk)
        self.assertEqual(student.first_name, update_data['first_name'])
        self.assertEqual(student.last_name, update_data['last_name'])

    def test_add_grade(self):
        student = Student.objects.create(**self.test_data)
        update_data = {
            'grades': [self.grade1.pk]
        }
        response = self.client.put(reverse(self.detail_url_name, kwargs={'pk': student.pk}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student = Student.objects.get(pk=student.pk)
        self.assertEqual(list(student.grades.all()), [self.grade1])

    def test_del_grade(self):
        student = Student.objects.create(**self.test_data)
        student.grades.add(self.grade1)
        self.assertEqual(list(student.grades.all()), [self.grade1])
        update_data = {
            'grades': []
        }
        response = self.client.put(reverse(self.detail_url_name, kwargs={'pk': student.pk}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student = Student.objects.get(pk=student.pk)
        self.assertEqual(list(student.grades.all()), [])


class GradeAPITestCase(APITestCase):
    list_url_name = 'grade-list'
    detail_url_name = 'grade-detail'

    def setUp(self):
        super(GradeAPITestCase, self).setUp()
        self.specialization1 = Specialization.objects.create(title='Английский язык')
        self.specialization2 = Specialization.objects.create(title='Математика')
        self.teacher = Teacher.objects.create(
            first_name='Иван',
            last_name='Иванов',
        )
        self.teacher.specializations.add(self.specialization1)
        self.teacher.specializations.add(self.specialization2)

    def createGrade(self):
        return Grade.objects.create(
            title='5а',
            specialization=self.specialization1,
            teacher=self.teacher
        )

    def test_get_list(self):
        response = self.client.get(reverse(self.list_url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        self.createGrade()
        response = self.client.get(reverse(self.list_url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_teacher(self):
        grade1 = self.createGrade()
        teacher2 = Teacher.objects.create(
            first_name='Иван',
            last_name='Иванов',
        )
        teacher2.specializations.add(self.specialization2)
        grade2 = Grade.objects.create(
            title='5б',
            teacher=teacher2,
            specialization=self.specialization2
        )
        response = self.client.get(reverse(self.list_url_name), {'teacher': self.teacher.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response = self.client.get(reverse(self.list_url_name), {'teacher': [self.teacher.pk, teacher2.pk]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        response = self.client.post(reverse(self.list_url_name), {
            'title': '5а',
            'specialization': self.specialization1.pk,
            'teacher': self.teacher.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.all().count(), 1)

    def test_create_with_invalid_specialization(self):
        specialization3 = Specialization.objects.create(title='Физика')
        response = self.client.post(reverse(self.list_url_name), {
            'title': '5а',
            'specialization': specialization3.pk,
            'teacher': self.teacher.pk
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Grade.objects.all().count(), 0)

    def test_get(self):
        grade = self.createGrade()
        response = self.client.get(reverse(self.detail_url_name, kwargs={'pk': grade.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], grade.pk)

    def test_delete(self):
        grade = self.createGrade()
        response = self.client.delete(reverse(self.detail_url_name, kwargs={'pk': grade.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Grade.objects.count(), 0)

    def test_update(self):
        grade = self.createGrade()
        update_data = {
            'title': '6а',
            'specialization': self.specialization2.pk,
            'teacher': self.teacher.pk
        }
        response = self.client.put(reverse(self.detail_url_name, kwargs={'pk': grade.pk}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        grade = Grade.objects.get(pk=grade.pk)
        self.assertEqual(grade.title, update_data['title'])
        self.assertEqual(grade.specialization.pk, update_data['specialization'])


class SpecializationAPITestCase(APITestCase):
    list_url_name = 'specialization-list'
    detail_url_name = 'specialization-detail'
    test_data = {
        'title': 'Математика',
    }

    def createSpecialization(self):
        return Specialization.objects.create(**self.test_data)

    def test_get_list(self):
        response = self.client.get(reverse(self.list_url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        self.createSpecialization()
        response = self.client.get(reverse(self.list_url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create(self):
        response = self.client.post(reverse(self.list_url_name), self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Specialization.objects.all().count(), 1)

    def test_get(self):
        specialization = self.createSpecialization()
        response = self.client.get(reverse(self.detail_url_name, kwargs={'pk': specialization.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], specialization.pk)

    def test_delete(self):
        specialization = self.createSpecialization()
        response = self.client.delete(reverse(self.detail_url_name, kwargs={'pk': specialization.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Specialization.objects.count(), 0)

    def test_update(self):
        specialization = self.createSpecialization()
        update_data = {
            'title': 'Физика',
        }
        response = self.client.put(reverse(self.detail_url_name, kwargs={'pk': specialization.pk}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        specialization = Specialization.objects.get(pk=specialization.pk)
        self.assertEqual(specialization.title, update_data['title'])
