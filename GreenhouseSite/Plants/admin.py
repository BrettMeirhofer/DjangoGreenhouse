from django.contrib import admin
from . import models


@admin.register(models.PlantStatus)
class PlantStatusAdmin(admin.ModelAdmin):
    list_display = ["status_name"]


@admin.register(models.PlantType)
class PlantTypeAdmin(admin.ModelAdmin):
    list_display = ["type_name", "determinate", "info_url"]


@admin.register(models.Plant)
class PlantAdmin(admin.ModelAdmin):
    list_filter = ["plant_status"]
    list_display = ["plant_type", "plant_status", "date_sprouted"]
