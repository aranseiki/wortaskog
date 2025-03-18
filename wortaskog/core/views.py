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
    current_year = datetime.now().year

    # Initialize form
    form = WorkLogForm(request.POST or None)

    # Default data: Full data for a GET request
    work_logs = WorkLog.objects.all()  # Fetch all work logs initially
    if request.method == 'POST':
        # breakpoint()  # Debugging
        # if request.POST['MyQueryInput']:  # Ensure the form has MyQueryInput
        sql_query = request.POST.get("MyQueryInput", "").strip()

        print(sql_query, '\n')  # Debugging

        if (sql_query) and (sql_query.lower().startswith('select')):
            try:
                work_logs = WorkLog.objects.raw(sql_query)
                request.POST = []  # Clear the POST data to avoid re-execution of the query
            except Exception as e:
                messages.error(request, f"SQL Error: {e}")
        else:
            messages.error(request, "Invalid SQL query.")  # Error message if no SQL query is entered
        # else:
            # print(form.errors, '\n')  # Debugging
            # messages.error(request, "Invalid SQL query.")

    # Render the page with the current data (filtered or full)
    context = {
        'year': current_year,
        'work_logs': work_logs,
    }

    return render(request, 'core/logview.html', context)
