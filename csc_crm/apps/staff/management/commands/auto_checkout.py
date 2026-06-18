from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, time

from csc_crm.apps.staff.models import Attendance


class Command(BaseCommand):

    help = "Auto checkout pending attendance"

    def handle(self, *args, **kwargs):

        pending_attendance = Attendance.objects.filter(
            log_in__isnull=False,
            log_out__isnull=True
        )

        for attendance in pending_attendance:

            auto_logout_time = datetime.combine(
                attendance.date,
                time(18, 30)
            )

            auto_logout_time = timezone.make_aware(
                auto_logout_time
            )

            attendance.log_out = auto_logout_time

            # Working hours calculate
            worked_time = (
                attendance.log_out -
                attendance.log_in
            )

            worked_hours = (
                worked_time.total_seconds() / 3600
            )

            # Less than 4 hours = Absent
            if worked_hours < 4:
                attendance.status = 'Absent'

            attendance.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Auto checkout completed successfully."
            )
        )