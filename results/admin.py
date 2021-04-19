from django.contrib import admin
from .models import AllureResult


@admin.register(AllureResult)
class AllureResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'results', 'uploaded_at')

