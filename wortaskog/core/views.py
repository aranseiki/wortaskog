from core.models import WorkLog, WorkLogForm
from core.export_view_db_route import WorkLogExportView
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse, StreamingHttpResponse
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


def view_worklogs(request):
    # Import CSV module
    import csv
    # Get current year
    current_year = datetime.now().year

    # Initialize form
    form = WorkLogForm(request.POST or None)

    # Default data: Full data for a GET request
    work_logs = WorkLog.objects.using('default').all()

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
                        filtered_work_logs = WorkLog.objects.raw(sql_query)

                        # Update the work logs to show the filtered results
                        work_logs = filtered_work_logs
                    except Exception as e:
                        # Error message if the SQL query is invalid
                        messages.error(request, f"SQL Error: {e}")
                else:
                    # Error message if no valid SQL query is entered
                    messages.error(request, "Invalid SQL query.")

            # Clear the work logs view database
            WorkLogExportView().export_view_db_clear()

            # Update the work logs view database
            WorkLogExportView().export_view_write(work_logs)

        # Check if the 'Exportar' button was clicked
        if action.upper() == 'EXPORTBUTTON':
            # Get the filtered work logs if they exist
            filtered_work_logs = WorkLogExportView().export_view_read()

            if not filtered_work_logs:
                filtered_work_logs = WorkLog.objects.using('default').all()

            # Write the data rows in the CSV file
            response = export_worklogs_csv(filtered_work_logs)

            # Return the CSV file as a download
            return response

    # Render the page with the current data (filtered or full)
    context = {
        'year': current_year,
        'work_logs': work_logs,
    }

    # Render the template with the context
    return render(request, 'core/logview.html', context)


def generate_csv(work_logs):
    """ Generator function for efficient CSV streaming. """
    yield (
        'Project Name,Month Worked,Date Worked,Hours Worked,'
        'Task Descriptions,Observations\n'
    )
    for log in work_logs:
        yield (
            f'{log.project_name},'
            f'{log.month_index},'
            f'{log.date_worked},'
            f'{log.hours_worked},'
            f'"{log.task_descriptions}"'
            f',"{log.observations}"'
            f'\n'
        )


def export_worklogs_csv(filtered_work_logs: list):
    """Export the work logs to a CSV file."""
    WorkLogfile = f'work_logs_{datetime.now().strftime("%d-%m-%Y")}.csv'

    response = StreamingHttpResponse(
        generate_csv(filtered_work_logs), content_type="text/csv"
    )
    response['Content-Disposition'] = (
        f'attachment; filename="{WorkLogfile}"'
    )
    return response
