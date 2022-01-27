from django.db import models
import datetime
from django import template
from Sensors.views.view_helpers import find_soil_status

register = template.Library()


class PlantType(models.Model):
    type_name = models.CharField(max_length=40)
    type_desc = models.CharField(max_length=200, null=True, blank=True)
    info_url = models.URLField(max_length=200)
    determinate = models.BooleanField()

    def __str__(self):
        return self.type_name


class PlantStatus(models.Model):
    status_name = models.CharField(max_length=40)

    def __str__(self):
        return self.status_name


class Plant(models.Model):
    plant_type = models.ForeignKey(PlantType, on_delete=models.RESTRICT, default=1)
    plant_status = models.ForeignKey(PlantStatus, on_delete=models.RESTRICT, default=1)
    soil_sensor = models.ForeignKey("Sensors.Sensor", on_delete=models.RESTRICT, default=1, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    date_sprouted = models.DateField(null=True, blank=True)
    date_died = models.DateField(null=True, blank=True)

    def age(self):
        delta = datetime.datetime.now().date() - self.date_sprouted
        return delta.days

    def soil_status(self):
        if self.soil_sensor is None:
            return "NA"
        else:
            return find_soil_status(self.soil_sensor.latest_value())
