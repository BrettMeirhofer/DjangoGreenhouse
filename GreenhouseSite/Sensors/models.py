from django.db import models
import os
import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class SensorType(models.Model):
    type_name = models.CharField(max_length=40)

    def __str__(self):
        return self.type_name


# Describes hardware that takes readings
class Sensor(models.Model):
    sensor_type = models.ForeignKey(SensorType, on_delete=models.RESTRICT, default=1)
    sensor_name = models.CharField(max_length=40)

    def __str__(self):
        return self.sensor_name

    def latest_value(self):
        return Reading.objects.filter(sensor_id=self.id).latest("reading_datetime").value


# Describes a measurement taken by a sensor at a date_time
class Reading(models.Model):
    value = models.FloatField(max_length=40)
    sensor = models.ForeignKey(Sensor, on_delete=models.RESTRICT, default=1)
    reading_datetime = models.DateTimeField()

    def __str__(self):
        return str(self.reading_datetime) + str(self.sensor) + str(self.value)


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


class Camera(models.Model):
    camera_name = models.CharField(max_length=40)

    def __str__(self):
        return self.camera_name


class DatedImage(models.Model):
    date = models.DateField()
    image = models.ImageField(upload_to='images/')
    thumb = models.ImageField(upload_to='images/thumbs/', null=True, blank=True)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True)

    def get_header(self):
        if self.camera is not None:
            return str(self.camera) + " " + str(self.date)
        else:
            return str(self.date)

    def make_thumbnail(self):
        thumb_size = 160, 120
        image = Image.open(self.image)
        image.thumbnail(thumb_size, Image.ANTIALIAS)

        thumb_name = os.path.basename(self.image.name)
        thumb_extension = os.path.splitext(thumb_name)[1]
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumb.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


class Tank(models.Model):
    level_sensor = models.ForeignKey(Sensor, on_delete=models.RESTRICT, null=True, blank=True, related_name="level")
    ph_sensor = models.ForeignKey(Sensor, on_delete=models.RESTRICT, null=True, blank=True, related_name="ph")
    ppm_sensor = models.ForeignKey(Sensor, on_delete=models.RESTRICT, null=True, blank=True, related_name="ppm")
    height = models.FloatField(max_length=40, null=True, blank=True)
    width = models.FloatField(max_length=40, null=True, blank=True)
    length = models.FloatField(max_length=40, null=True, blank=True)
    sensor_dist = models.FloatField(max_length=40, null=True, blank=True)
    default_ppm = models.IntegerField(default=150)
    default_ph = models.FloatField(max_length=40, default=7)

    target_ppm = models.IntegerField(default=500)
    target_ph = models.FloatField(max_length=40, default=6.5)


    n = models.IntegerField(default=0)
    p = models.IntegerField(default=0)
    k = models.IntegerField(default=0)













