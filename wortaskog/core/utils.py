# Import type hints for generator and iterable types
from typing import Generator, Iterable

# Import the WorkLog model to access work log data
from core.models import WorkLog


# Define a generator function to efficiently stream CSV content
def generate_csv(work_logs: Iterable[WorkLog]) -> Generator[str, None, None]:
    # Yield the CSV header row with column names
    yield (
        'Project Name,'
        'Month Worked,'
        'Date Worked,'
        'Hours Worked,'
        'Task Descriptions,'
        'Observations'
        '\n'
    )

    # Iterate through each work log entry in the iterable
    for log in work_logs:
        # Yield a formatted CSV row for the current work log entry
        yield (
            f'{log.project_name},'
            f'{log.month_index},'
            f'{log.date_worked},'
            f'{log.hours_worked},'
            f'"{log.task_descriptions}"'
            f',"{log.observations}"'
            f'\n'
        )
