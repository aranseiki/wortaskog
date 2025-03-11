from core.models import WorkLog, WorkLogForm
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect, render


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


def insert_worklogs(request):
    # Get current year
    current_year = datetime.now().year

    # Initialize form and result_form
    form = WorkLogForm(request.POST or None)
    result_form = None

    # Handle form submission
    if request.method == 'POST' and form.is_valid():
        # Save the new work log to the database
        form.save()
        # Set the success message
        messages.success(request, 'Work log added successfully!')
        # Redirect to the same page to clear the form
        response = redirect('loginsert')
    else:
        # Create the context with all objects and the form:
            # current_year pass the current year
            # result_form pass the success message to the template
            # form pass the form to the template
        context = {
            'year': current_year,
            'result_form': result_form,
            'form': form,
        }

        # Render the template with the context
        response = render(
            request = request,
            template_name = 'core/loginsert.html',
            context = context,
        )

    return response


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
