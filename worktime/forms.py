# coding: utf-8
from django import forms
from worktime.models import Employee


class DatepickerWidget(forms.TextInput):

    class Media:
        css = {'all': ('//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css',)}
        js = ('https://code.jquery.com/jquery-1.12.4.js', 'https://code.jquery.com/ui/1.12.1/jquery-ui.js')


class PeriodForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(PeriodForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    employee = forms.ModelChoiceField(queryset=Employee.objects.all().only('id', 'lastname'), label=u'Сотрудник')
    period = forms.CharField(widget=DatepickerWidget, label=u'Период')

    def clean_period(self):
        data = self.cleaned_data['period']
        period = data.split('-')
        for data in period:
            if int(data[:2]) > 31 or int(data[2:4]) > 12 or int(data[:2]) < 1 or int(data[2:4]) < 1:
                raise forms.ValidationError('Неверный период!!!')
        return period


class EmployeeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Employee
        fields = ['company', 'firstname', 'lastname', 'post', 'start_work', 'end_work', 'card']
