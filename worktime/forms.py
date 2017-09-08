# coding: utf-8
from django import forms
from worktime.models import Employee


class DatepickerWidget(forms.TextInput):

    class Media:
        css = {'all': ('//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css',)}
        js = ('https://code.jquery.com/jquery-1.12.4.js', 'https://code.jquery.com/ui/1.12.1/jquery-ui.js')


class AddCssClass(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AddCssClass, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PeriodForm(AddCssClass):

    employee = forms.ModelChoiceField(queryset=Employee.objects.all().only('id', 'lastname'), label=u'Сотрудник')
    # employee = forms.CharField(widget=DatepickerWidget, label=u'Сотрудник')
    period = forms.CharField(widget=DatepickerWidget, label=u'Период')

    def clean_period(self):
        data = self.cleaned_data['period']
        period = data.split('-')
        for data in period:
            if int(data[:2]) > 31 or int(data[2:4]) > 12 or int(data[:2]) < 1 or int(data[2:4]) < 1:
                raise forms.ValidationError('Неверный период!!!')
        if len(period) < 2:
            period.append(period[0])
        return period


class EmployeeUpdateForm(forms.ModelForm, AddCssClass):

    class Meta:
        model = Employee
        fields = ['company', 'firstname', 'lastname', 'post', 'start_work', 'end_work', 'card']


class EmployeeCreateForm(EmployeeUpdateForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeCreateForm, self).__init__(*args, **kwargs)
        self.fields['card'].initial = '300000000'

    def clean_card(self):
        card = self.cleaned_data['card']
        if not len(card) == 13:
            raise forms.ValidationError('Некорректный номер карты!')
        try:
            employee = Employee.objects.get(card=card)
        except Employee.DoesNotExist:
            employee = None
        if employee:
            raise forms.ValidationError(u'Карта %s уже зарегистрирована на сотрудника %s!' % (card, employee))
        return card
