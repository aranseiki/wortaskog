# Import the datetime class to handle date and time operations
from datetime import datetime

# Import the WorkLog model and WorkLogForm form class from the core app
from core.models import WorkLog, WorkLogForm

# Import the custom view responsible for exporting work logs
from core.export_view_db_route import WorkLogExportView

# Import Django's message framework to provide user feedback
from django.contrib import messages

# Import the decorator to enforce login requirement on views
from django.contrib.auth.decorators import login_required

# Import redirect and render functions to manage HTTP responses
from django.shortcuts import redirect, render

# Import the function responsible for exporting work logs as CSV
from core.exporters import export_worklogs_csv


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


@login_required
def insert_worklogs(request):
    # Get current year
    current_year = datetime.now().year

    # Initialize form and result_form
    form = WorkLogForm(request.POST or None)

    # default value for result_form
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

    # return the response to html page
    return response


@login_required
def view_worklogs(request):
    # Import CSV module
    import csv
    # Get current datetime
    current_datetime = datetime.now()

    # Get current year
    current_year = current_datetime.year

    # Initialize User data
    user = request.user

    # Default data: Full data for a GET request
    work_logs = WorkLog.objects.using('default').all().filter(user=user)

    # Handle form submission
    if request.method == 'POST':
        action = request.POST.get('action', '')

        # Check if the 'Exportar' button was clicked
        if action.upper() == 'RUNQUERYBUTTON':
            # Check if the 'Run Query' button was clicked
            sql_query = request.POST.get("MyQueryInput", "").strip()

            # Check if the SQL query is not empty
            if not sql_query == '':
                # Check if the SQL query is a SELECT statement
                if sql_query.upper().startswith('SELECT '):
                    try:
                        # Apply the SQL query to filter work logs
                        filtered_work_logs = WorkLog.objects.filter(user=user).raw(sql_query)

                        # Update the work logs to show the filtered results
                        work_logs = filtered_work_logs
                    except Exception as e:
                        # Error message if the SQL query is invalid
                        messages.error(request, f"SQL Error: {e}")
                else:
                    # Error message if no valid SQL query is entered
                    messages.error(request, "Invalid SQL query.")

            # Clear the work logs view database
            WorkLogExportView().export_view_db_clear(user = user)

            # Update the work logs view database
            WorkLogExportView().export_view_write(default_db_result = work_logs, user = user)

        # Check if the 'Exportar' button was clicked
        if action.upper() == 'EXPORTBUTTON':
            # Get the filtered work logs if they exist
            filtered_work_logs = WorkLogExportView().export_view_read(user = user)

            if not filtered_work_logs:
                filtered_work_logs = WorkLog.objects.using('default').all().filter(user=user)

            # Write the data rows in the CSV file
            response = export_worklogs_csv(
                filtered_work_logs,
                current_datetime= current_datetime,
            )

            # Return the CSV file as a download
            return response

    # Render the page with the current data (filtered or full)
    context = {
        'year': current_year,
        'work_logs': work_logs,
    }

    # Render the template with the context
    return render(request, 'core/logview.html', context)
