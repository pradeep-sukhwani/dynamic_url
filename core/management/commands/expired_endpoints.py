from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from core.models import URL


class Command(BaseCommand):
    help = 'Delete the URL and URLDetails if the created on is more than 1 hour.'

    def handle(self, *args, **options):
        url_queryset = URL.objects.all()
        for item in url_queryset:
            created_on_ahead_one_hour = item.created_on + timedelta(hours=1)
            current_datetime = datetime.now().astimezone()
            if item.created_on <= created_on_ahead_one_hour and created_on_ahead_one_hour >= current_datetime:
                continue
            self.stdout.write(self.style.SUCCESS(item.endpoint) + " ")
            item.url_details.all().delete()
            item.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all the endpoints who were created an hour back.'))
        return
