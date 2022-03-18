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


# Looking for a way to bulk save but .update() doesn't work because the field changes are in the func params
# Instead of saving any modified fields
@admin.action(description='Create thumbnails for images')
def make_thumb(modeladmin, request, queryset):
    for x in list(queryset):
        x.make_thumbnail()
        x.save()


@admin.register(models.DatedImage)
class DatedImageAdmin(admin.ModelAdmin):
    list_display = ["date", "camera"]
    actions = [make_thumb]


admin.site.register(models.SensorType)
admin.site.register(models.Device)
admin.site.register(models.Camera)
admin.site.register(models.Tank)
