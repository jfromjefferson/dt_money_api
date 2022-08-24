from django.contrib import admin
from . import models

# Register your models here.


class OwnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'uuid']


class SysUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'uuid']


admin.site.register(models.Owner, OwnerAdmin)
admin.site.register(models.SysUser, SysUserAdmin)
admin.site.register(models.Transaction)
