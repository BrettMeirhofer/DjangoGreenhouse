from django.core.management.base import BaseCommand
from django.db.models import Count
from Sensors import models
from datetime import timedelta, datetime
from django.utils.timezone import utc


# Set the sensor for temp/humd readings from Lower/Electronics to the four sensors that correspond to the readingtype
class Command(BaseCommand):
    help = 'Displays stats related to Article and Comment models'

    def handle(self, *args, **kwargs):
        names = ["Lower", "Electronics", "Greenhouse Temperature", "Greenhouse Humidity", "Electronics Temperature", "Electronics Humidity"]
        type_names = ["Temperature", "Humidity"]
        types = []
        sensors = []

        for name in names:
            sensors.append(models.Sensor.objects.get(sensor_name=name).id)

        for type_name in type_names:
            types.append(models.ReadingType.objects.get(type_name=type_name).id)

        remaps = [
            {"id": sensors[0],
             "sensor_types": [{"type": types[0], "sensor": sensors[2]}, {"type": types[1], "sensor": sensors[3]}]
             },
            {"id": sensors[1],
             "sensor_types": [{"type": types[0], "sensor": sensors[4]}, {"type": types[1], "sensor": sensors[5]}]
             }
        ]

        for remap in remaps:
            for sensor_type in remap["sensor_types"]:
                readings = models.Reading.objects.filter(sensor_id=remap["id"]).filter(reading_type_id=sensor_type["type"])
                readings.update(sensor_id=sensor_type["sensor"])
                models.Reading.objects.bulk_update(readings, ["sensor_id"])
