from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from core.models import WorkLog


def home(request):
    # Get current year
    current_year = datetime.now().year

    # Create the context with all objects
    context = {
        'year': current_year,
    }

    # render all passing object to template
    return render(
        request = request,
        template_name = 'core/home.html',
        context = context,
    )


def view_worklogs(request):
    # Get all work logs
    work_logs = WorkLog.objects.all()
    
    # Get current year
    current_year = datetime.now().year

    # Create the context with all objects
    context = {
        'year': current_year,
        'work_logs': work_logs,
    }

    # render all passing object to template
    return render(
        request = request,
        template_name = 'core/logview.html',
        context = context,
    )
