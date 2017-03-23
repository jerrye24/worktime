#coding: utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
from django.views.generic.dates import DayArchiveView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from worktime.models import Employee, Tabel
from worktime.forms import RegistrationForm, PeriodForm
import datetime
from django.utils import timezone
import openpyxl
from worktime.functions import time_delta, hello_message


def custom_login(request):
    username = request.POST['username']
    password = request.POST['password']
    date = datetime.date.today()
    user = authenticate(username=username, password=password)
    if user is not None:
	if user.is_active:
	    login(request, user)
	    return redirect('tabel', year=date.year, month=date.month, day=date.day)
    else:
	return redirect('index')


def index(request):
    if request.method == 'POST':
	card = request.POST['card']
	time = timezone.localtime(timezone.now())
        try:
	    employee = Employee.objects.get(card=card)
	except Employee.DoesNotExist:
	    return render(request, 'worktime/error.html')
	try:
	    tabel = Tabel.objects.get(employee=employee, start_work__gte=datetime.date.today(), at_work=True)
	    tabel.end_work = timezone.now()
	    tabel.at_work = False
	    tabel.time_at_work = time_delta(tabel.end_work - tabel.start_work)
	    tabel.save()
	    message = ['До свидания,', 'Всего хорошего,', 'До скорой встречи, ;)', 'До встречи,']
	    return render(request, 'worktime/bye.html', {'employee': employee, 'message': message})
	except Tabel.DoesNotExist:
	    tabel = Tabel(employee=employee, at_work=True)
	    tabel.save()
	    message = hello_message(time)
	    return render(request, 'worktime/hello.html', {'employee': employee, 'message': message})
    return render(request, 'worktime/index.html')


class TabelView(LoginRequiredMixin, DayArchiveView):
    model = Tabel
    date_field = 'start_work'
    template_name = 'worktime/tabel.html'
    context_object_name = 'tabel_table'
    allow_empty = True
    allow_future = True
    month_format = '%m'


class EmployeeView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'worktime/employee.html'
    context_object_name = 'employee_table'


class EmployeeSearchView(LoginRequiredMixin, ListView):
    template_name = 'worktime/employee.html'
    context_object_name = 'employee_table'
    
    def get_queryset(self):
	return Employee.objects.filter(lastname__istartswith=self.args[0])


@login_required
def tabel_period_form(request):
    if request.method == 'POST':
        form = PeriodForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            period = data['period']
            start = period[0]
            try:
                end = period[1]
            except ImportError:
                end = start
            return redirect('tabel_period', start=start, end=end, id=data['employee'].id)
    else:
        form = PeriodForm()
    return render(request, 'worktime/period_form.html', {'form': form})


@login_required
def tabel_period(request, start, end, id):
    start = datetime.date(int(start[4:]), int(start[2:4]), int(start[:2]))
    end = datetime.datetime(int(end[4:]), int(end[2:4]), int(end[:2]), 23, 59)
    tabel_period = Tabel.objects.filter(employee=id, start_work__range=(start, end))
    employee = Employee.objects.get(id=id)
    return render(request, 'worktime/tabel_period.html', {'tabel_period': tabel_period, 'start': start, 'end': end, 'employee': employee})


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    fields = ['company', 'lastname', 'firstname', 'post', 'start_work', 'end_work', 'card']
    success_url = '/employee/'
    template_name = 'worktime/employee_create.html'


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    fields = ['company', 'lastname', 'firstname', 'post', 'start_work', 'end_work', 'card']
    success_url = '/employee/'
    template_name = 'worktime/employee_update.html'


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'worktime/employee_delete.html'


@login_required
def export_xlsx(request, year, month, day):
    date = datetime.date(int(year), int(month), int(day))
    tabel = Tabel.objects.filter(start_work__contains=date).order_by('employee')
    excel_data = [[u'Сотрудник', u'Начало смены', u'Конец смены', u'Длительность смены', 'Дата'],
		  ['', '', '', '', '']
		 ]
    for obj in tabel:
	if obj.end_work:
	    end_work = '{}:{:0>2}'.format(timezone.localtime(obj.end_work).hour, obj.end_work.minute)
	else:
	    end_work = ''
	excel_data.append([str(obj.employee),
			  '{}:{:0>2}'.format(timezone.localtime(obj.start_work).hour, obj.start_work.minute),
			  end_work,
			  str(obj.time_at_work),
			  str(obj.start_work.date())
			])
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    ws.title = u'Табель %s' % date
    ws.column_dimensions['A'].width = 40
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 15
    for line in excel_data:
	ws.append(line)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % date
    
    wb.save(response)
    return response