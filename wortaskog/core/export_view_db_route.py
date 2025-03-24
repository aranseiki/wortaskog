from core.models import WorkLog
from django.db import transaction

class WorkLogExportView:
    """Handles exporting work logs to a temporary database. """

    @staticmethod
    def export_view_read():
        """Reads all work logs from the temp database."""
        return WorkLog.objects.using('export_view_db').all()

    @staticmethod
    def export_view_write(default_db_result):
        """Writes filtered work logs to the temp database."""
        with transaction.atomic(using='export_view_db'):
            WorkLog.objects.using('export_view_db').bulk_create(default_db_result)

    @staticmethod
    def export_view_db_clear():
        """Clears all data from the temp database."""
        with transaction.atomic(using='export_view_db'):
            WorkLog.objects.using('export_view_db').all().delete()

