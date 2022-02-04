from django.core.management.base import BaseCommand
from django.db.models import Count
from Sensors import models
from datetime import timedelta, datetime
from django.utils.timezone import utc


# Sets all the reading_type fields to null in preparation for removing it entirely
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        readings = models.Reading.objects.all()
        readings.update(reading_type=None)
        models.Reading.objects.bulk_update(readings, ["reading_type"])