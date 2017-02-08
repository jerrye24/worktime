#coding: utf8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Employee(models.Model):
    company = models.CharField(default='Галс', max_length=10, verbose_name='Компания')
    firstname = models.CharField(max_length=20, verbose_name='Имя')
    lastname = models.CharField(max_length=20, verbose_name='Фамилия')
    post = models.CharField(max_length=50, verbose_name='Должность')
    start_work = models.TimeField(default='10:30:00', verbose_name='Начало смены')
    end_work = models.TimeField(default='19:30:00', verbose_name='Конец смены')
    card = models.CharField(max_length=13, verbose_name='Карта сотрудника')

    def __str__(self):
        return '%s %s' % (self.lastname, self.firstname)

    class Meta:
        ordering = ['lastname']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


@python_2_unicode_compatible
class Tabel(models.Model):
    employee = models.ForeignKey(Employee, verbose_name='Сотрудник')
    start_work = models.DateTimeField(auto_now_add=True, verbose_name='Начало смены')
    end_work = models.DateTimeField(null=True, verbose_name='Конец смены')
    time_at_work = models.TimeField(null=True, verbose_name='Длительность смены')
    at_work = models.BooleanField(verbose_name='На работе')

    def __str__(self):
        return '%s' % self.employee

    class Meta:
	ordering = ['employee']
        verbose_name = 'Табель'
        verbose_name_plural = 'Табели'