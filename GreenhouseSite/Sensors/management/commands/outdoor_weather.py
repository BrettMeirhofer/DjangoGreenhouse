from django.core.management.base import BaseCommand
from Sensors.views import view_helpers as helpers


# Sets all the reading_type fields to null in preparation for removing it entirely
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        helpers.get_outdoor_weather()
