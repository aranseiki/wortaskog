# Import the datetime class to handle formatted timestamps
from datetime import datetime

# Import Iterable for type hinting iterable arguments
from typing import Iterable

# Import HTTP response classes from Django
from django.http import HttpResponse, StreamingHttpResponse

# Import the WorkLog model that holds the work log data
from core.models import WorkLog

# Import the CSV generator function
from core.utils import generate_csv


# Define a function to export work logs as a CSV file
def export_worklogs_csv(
    filtered_work_logs: Iterable[WorkLog],
    current_datetime: datetime,
) -> HttpResponse:

    # Format the filename with the current date
    worklog_filename = f'work_logs_{current_datetime.strftime("%d-%m-%Y")}.csv'

    # Create a streaming HTTP response with the CSV data
    response = StreamingHttpResponse(
        generate_csv(filtered_work_logs),
        content_type="text/csv"
    )

    # Add content-disposition header to force file download with the specified name
    response['Content-Disposition'] = (
        f'attachment; filename="{worklog_filename}"'
    )

    # Return the final HTTP response containing the CSV file
    return response
