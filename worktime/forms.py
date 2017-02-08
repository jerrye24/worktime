#coding: utf-8
from django import forms
from worktime.models import Employee


class RegistrationForm(forms.Form):
	card = forms.CharField(label='Карта сотрудника', max_length=13)


class DatepickerWidget(forms.TextInput):
    class Media:
        css = {'all': ('//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css', )}
        js = ('https://code.jquery.com/ui/1.12.1/jquery-ui.js', )


class PeriodForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all().only('id', 'lastname'), label=u'Сотрудник')
    period = forms.CharField(widget=DatepickerWidget, label=u'Период')

    def clean_period(self):
        data = self.cleaned_data['period']
        period = data.split('-')
        for data in period:
            if int(data[:2]) > 31 or int(data[2:4]) > 12 or int(data[:2]) < 1 or int(data[2:4]) < 1:
                raise forms.ValidationError('Неверный период!!!')
        return period
