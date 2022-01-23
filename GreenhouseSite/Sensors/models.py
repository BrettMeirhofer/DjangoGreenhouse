from django.db import models


class SensorType(models.Model):
    type_name = models.CharField(max_length=40)

    def __str__(self):
        return self.type_name


# Describes what a reading measures
class ReadingType(models.Model):
    type_name = models.CharField(max_length=40)

    def __str__(self):
        return self.type_name


# Describes hardware that takes readings
class Sensor(models.Model):
    sensor_type = models.ForeignKey(SensorType, on_delete=models.RESTRICT, default=1)
    sensor_name = models.CharField(max_length=40)

    def __str__(self):
        return self.sensor_name


# Describes a measurement taken by a sensor at a date_time
class Reading(models.Model):
    value = models.FloatField(max_length=40)
    sensor = models.ForeignKey(Sensor, on_delete=models.RESTRICT, default=1)
    reading_type = models.ForeignKey(ReadingType, on_delete=models.RESTRICT, default=1)
    reading_datetime = models.DateTimeField()

    def __str__(self):
        return str(self.reading_datetime) + str(self.reading_type) + str(self.sensor) + str(self.value)


# Describes a device that can be toggled
class Device(models.Model):
    device_name = models.CharField(max_length=40)

    def __str__(self):
        return self.device_name


# Describes the toggle status of a device at a date_time
class DeviceStatus(models.Model):
    device = models.ForeignKey(Device, on_delete=models.RESTRICT, default=1)
    status = models.BooleanField()
    status_datetime = models.DateTimeField()


class DatedImage(models.Model):
    date = models.DateField()
    image = models.ImageField(upload_to='images/')
