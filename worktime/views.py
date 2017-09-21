# coding: utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.generic.dates import DayArchiveView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Employee, Tabel
from .forms import PeriodForm, EmployeeCreateForm, EmployeeUpdateForm
import datetime
from django.utils import timezone
import openpyxl
from .functions import time_delta, hello_message


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
        except Employee.MultipleObjectsReturned:
            return render(request, 'worktime/error.html', {'card': card})
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
    date_field = 'start_work'
    template_name = 'worktime/tabel.html'
    context_object_name = 'tabel_table'
    allow_empty = True
    allow_future = True
    month_format = '%m'

    def get_context_data(self, **kwargs):
        context = super(TabelView, self).get_context_data(**kwargs)
        context['company_list'] = [i[0] for i in Employee.COMPANY]
        return context

    def get_queryset(self):
        company = self.request.GET.get('company')
        if company:
            return Tabel.objects.filter(employee__company=company)
        else:
            return Tabel.objects.all()


@login_required
def tabel_period_form(request):
    if request.method == 'POST':
        form = PeriodForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            return redirect('tabel_period', start=data['period'][0], end=data['period'][1], id=data['employee'])
    else:
        form = PeriodForm()
    return render(request, 'worktime/tabel_form.html', {'form': form})


@login_required
def tabel_json(request):
    term = request.GET['term'].capitalize()
    data = Employee.objects.filter(lastname__startswith=term)
    employees = []
    for employee in data:
        employee = {'value': str(employee), 'id': employee.id}
        employees.append(employee)
    return JsonResponse(employees, safe=False)


@login_required
def tabel_period(request, start, end, id):
    start = datetime.date(int(start[4:]), int(start[2:4]), int(start[:2]))
    end = datetime.datetime(int(end[4:]), int(end[2:4]), int(end[:2]), 23, 59)
    employee = Employee.objects.get(id=id)
    tabel_period = Tabel.objects.filter(employee=employee, start_work__range=(start, end))
    return render(request, 'worktime/tabel_period.html',
                  {'tabel_period': tabel_period, 'start': start, 'end': end, 'employee': employee})


@login_required
def employee_view(request):
    company_list = [i[0] for i in Employee.COMPANY]
    company = request.GET.get('company')
    lastname = request.GET.get('lastname')
    if company:
        employee_table = Employee.objects.filter(company=company)
    elif lastname:
        employee_table = Employee.objects.filter(lastname__istartswith=lastname)
    else:
        employee_table = Employee.objects.all()
    return render(request, 'worktime/employee.html', {'employee_table': employee_table, 'company_list': company_list})


@login_required
def employee_create_view(request):
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee')
        else:
            return render(request, 'worktime/employee_create.html', {'form': form})
    else:
        form = EmployeeCreateForm()
        return render(request, 'worktime/employee_create.html', {'form': form})


@login_required
def employee_update_view(request, pk):
    employee = Employee.objects.get(id=pk)
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST)
        if form.is_valid():
            form = EmployeeUpdateForm(request.POST, instance=employee)
            form.save()
            return redirect('employee')
        else:
            return render(request, 'worktime/employee_update.html', {'form': form})
    else:
        form = EmployeeUpdateForm(instance=employee)
        return render(request, 'worktime/employee_update.html', {'form': form})


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
