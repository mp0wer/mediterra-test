# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class Specialization(models.Model):
    title = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
        ordering = ['title']

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Teacher(models.Model):
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    specializations = models.ManyToManyField(Specialization, verbose_name='Специализации')

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return ' '.join((self.last_name, self.first_name))


@python_2_unicode_compatible
class Grade(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name='Учитель')
    specialization = models.ForeignKey(Specialization, verbose_name='Специализация')
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['title']

    def __str__(self):
        return self.title

    def clean(self):
        if self.teacher and self.specialization \
                and not self.teacher.specializations.filter(pk=self.specialization.pk).exists():
            raise ValidationError('Специализация класса должна совпадать с одной из специализаций учителя')


@python_2_unicode_compatible
class Student(models.Model):
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    grades = models.ManyToManyField(Grade, verbose_name='Классы', blank=True)

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return ' '.join((self.last_name, self.first_name))
