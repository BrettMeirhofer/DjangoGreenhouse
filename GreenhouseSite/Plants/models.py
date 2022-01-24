from django.db import models


class PlantType(models.Model):
    type_name = models.CharField(max_length=40)
    type_desc = models.CharField(max_length=200)
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
    notes = models.CharField(max_length=200)
    date_sprouted = models.DateField()
    date_died = models.DateField()
