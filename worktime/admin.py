# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Tabel, CustomUser


class AdminTabel(admin.ModelAdmin):
    list_display = ('employee', 'start_work')
    list_filter = ('start_work', )
    ordering = ('-start_work', )


class AdminCustomUser(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Разрешенные компании', {'fields': ('company_permission', )}),
    )


admin.site.register(Employee, )
admin.site.register(Tabel, AdminTabel)
admin.site.register(CustomUser, AdminCustomUser)

