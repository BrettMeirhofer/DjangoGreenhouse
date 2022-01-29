from django.db import models
import os
from io import BytesIO


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

    def latest_value(self):
        return Reading.objects.filter(sensor_id=self.id).latest("reading_datetime").value


# Describes a measurement taken by a sensor at a date_time
class Reading(models.Model):
    value = models.FloatField(max_length=40)
    sensor = models.ForeignKey(Sensor, on_delete=models.RESTRICT, default=1)
    reading_type = models.ForeignKey(ReadingType, on_delete=models.RESTRICT, default=1, null=True, blank=True)
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

    """
    thumbnail = models.ImageField(upload_to='thumbs', editable=False)

    def save(self, *args, **kwargs):

        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(DatedImage, self).save(*args, **kwargs)

    def make_thumbnail(self):

        image = Image.open(self.image)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension == '.png':
            FTYPE = 'PNG'



        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True
    """

