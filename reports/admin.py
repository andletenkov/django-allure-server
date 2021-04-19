from django.contrib import admin

from .models import AllureReport


@admin.register(AllureReport)
class AllureReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'path', 'report', 'created_at')
