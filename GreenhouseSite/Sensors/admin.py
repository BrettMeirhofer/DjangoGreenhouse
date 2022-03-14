from django.contrib import admin
from . import models


@admin.register(models.Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_filter = ["sensor"]
    list_display = [field.name for field in models.Reading._meta.get_fields()]
    
    
@admin.register(models.Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_filter = ["sensor_type"]
    list_display = ["sensor_name", "sensor_type"]


@admin.register(models.DeviceStatus)
class DeviceStatusAdmin(admin.ModelAdmin):
    list_filter = ["device"]
    list_display = ["device", "status", "status_datetime"]


@admin.register(models.DatedImage)
class DatedImageAdmin(admin.ModelAdmin):
    list_display = ["date"]


admin.site.register(models.SensorType)
admin.site.register(models.Device)
admin.site.register(models.Camera)
