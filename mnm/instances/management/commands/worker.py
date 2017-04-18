import traceback
import schedule
import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from django.conf import settings
from mnm.instances import tasks


class Command(BaseCommand):
    help = 'Fetch instance data regularly'

    def handle(self, *args, **options):
        schedule.every(1).hour.do(
            lambda: tasks.fetch_instances('instances_hourly')
        )
        schedule.every(settings.FETCH_DELAY).seconds.do(
            lambda: tasks.fetch_instances('instances')
        )
        schedule.every(settings.FETCH_COUNTRY_DELAY).seconds.do(
            lambda: tasks.fetch_instances_countries(empty=True, maximum=10)
        )
        schedule.every(settings.REFRESH_COUNTRY_DELAY).seconds.do(
            lambda: tasks.fetch_instances_countries(empty=False, maximum=10)
        )

        self.stdout.write(self.style.SUCCESS('Starting job runner...'))
        while True:
            time.sleep(1)
            try:
                schedule.run_pending()
            except:
                traceback.print_exc()