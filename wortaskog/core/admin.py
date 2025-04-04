from django.contrib import admin
from core.models import WorkLog


# Register the WorkLog model
@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'project_name',
        'month_index',
        'date_worked',
        'hours_worked',
        'task_descriptions',
        'observations',
    )
    list_filter = ('user',)
    search_fields = ('user__username', 'descricao')
