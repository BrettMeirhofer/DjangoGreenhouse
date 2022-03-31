from django.db import models
import datetime
from django import template
from Sensors.views.view_helpers import find_soil_status

register = template.Library()


# Describes the species or subspecies of the plant
class PlantType(models.Model):
    type_name = models.CharField(max_length=40)
    type_desc = models.CharField(max_length=200, null=True, blank=True)
    info_url = models.URLField(max_length=200, null=True, blank=True)
    determinate = models.BooleanField()
    preferred_ppm = models.IntegerField(default=500)
    preferred_ph = models.FloatField(max_length=40, default=6.5)

    def __str__(self):
        return self.type_name


# Describes the stage of growth the plant is in
class PlantStatus(models.Model):
    status_name = models.CharField(max_length=40)

    def __str__(self):
        return self.status_name


# Describes what material the plant is planted in
class PlantMedium(models.Model):
    medium_name = models.CharField(max_length=40)

    def __str__(self):
        return self.medium_name


# Describes a specific plant
class Plant(models.Model):
    type_id = models.IntegerField(null=True, blank=True)  # The id listed on the pot

    plant_type = models.ForeignKey(PlantType, on_delete=models.RESTRICT, default=1)
    plant_status = models.ForeignKey(PlantStatus, on_delete=models.RESTRICT, default=1)
    plant_medium = models.ForeignKey(PlantMedium, on_delete=models.SET_NULL, null=True, blank=True)
    tank = models.ForeignKey("Sensors.Tank", on_delete=models.RESTRICT, null=True, blank=True)
    soil_sensor = models.ForeignKey("Sensors.Sensor", on_delete=models.RESTRICT, null=True, blank=True)
    parent1 = models.ForeignKey('self', null=True, blank=True, related_name='children1', on_delete=models.SET_NULL)
    parent2 = models.ForeignKey('self', null=True, blank=True, related_name='children2', on_delete=models.SET_NULL)
    clone = models.BooleanField(default=False)

    planter_capacity = models.FloatField(default=0)

    date_sprouted = models.DateField(null=True, blank=True)
    date_died = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)

    def age(self):
        delta = datetime.datetime.now().date() - self.date_sprouted
        return delta.days

    def soil_status(self):
        if self.soil_sensor is None:
            return "NA"
        else:
            return find_soil_status(self.soil_sensor.latest_value())
