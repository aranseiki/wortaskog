from core.models import WorkLog, WorkLogForm
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
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
    # Import CSV module
    import csv
    # Get current year
    current_year = datetime.now().year

    # Initialize form
    form = WorkLogForm(request.POST or None)

    # Default data: Full data for a GET request
    work_logs = WorkLog.objects.all()

    # Handle form submission
    if request.method == 'POST':
        # Variable to keep track of the filtered results for export
        filtered_work_logs = None

        # Check if the 'Run Query' button was clicked
        sql_query = request.POST.get("MyQueryInput", "").strip()
        # Check if the SQL query is a SELECT statement
        if sql_query and sql_query.lower().startswith('select'):
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

        # Check if the 'Exportar' button was clicked
        if 'exportButton' in request.POST:
            # breakpoint()
            # Export the current filtered or full work logs to a CSV file
            filtered_work_logs = work_logs

            # Create CSV response for the current filtered or full work logs
            response = HttpResponse(content_type='text/csv')
            # Set the CSV file name
            response['Content-Disposition'] = 'attachment; filename="work_logs.csv"'

            # Create a CSV writer object
            writer = csv.writer(response)
            # Write the header row (columns)
            writer.writerow(
                [
                    'Project Name',
                    'Month Worked',
                    'Date Worked',
                    'Hours Worked',
                    'Task Descriptions',
                    'Observations'
                ]
            )

            # Write the data rows (use filtered_work_logs to export the result of the query)
            for log in filtered_work_logs:
                # Write each row with the work log data
                writer.writerow(
                    [
                        log.project_name,
                        log.month_index,
                        log.date_worked,
                        log.hours_worked,
                        log.task_descriptions,
                        log.observations
                    ]
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
