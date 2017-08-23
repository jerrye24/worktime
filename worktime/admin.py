from django.contrib import admin
from .models import Employee, Tabel


class AdminTabel(admin.ModelAdmin):
    list_display = ('employee', 'start_work')
    list_filter = ('start_work', )
    ordering = ('-start_work', )


admin.site.register(Employee)
admin.site.register(Tabel, AdminTabel)

