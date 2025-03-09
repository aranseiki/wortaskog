from django.db import models


class WorkLog(models.Model):
    # Fields
    # Name of the project
    project_name = models.CharField(max_length=100)
    # Index to each month (1-12)
    month_index = models.IntegerField()
    # Date of the work log
    date_worked = models.DateField()
    # Hours worked
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    # Optional observations
    task_descriptions = models.TextField(blank=True, null=True)
    # Optional observations
    observations = models.TextField(blank=True, null=True)

    # Metadata
    class Meta:
        # Order logs by date (newest first)
        ordering = ['-date_worked']

    # String representation
    def __str__(self):
        return f"{self.project_name} - {self.date_worked}"