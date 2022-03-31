from django.contrib import admin
from . import models


@admin.register(models.PlantStatus)
class PlantStatusAdmin(admin.ModelAdmin):
    list_display = ["status_name"]


@admin.register(models.PlantType)
class PlantTypeAdmin(admin.ModelAdmin):
    list_display = ["type_name", "determinate", "info_url"]


@admin.action(description='Duplicates selected plants and saves them')
def copy_plants(modeladmin, request, queryset):
    for x in list(queryset):
        x.pk = None
        x.save()


@admin.register(models.Plant)
class PlantAdmin(admin.ModelAdmin):
    list_filter = ["plant_status"]
    list_display = ["plant_type", "type_id", "plant_medium", "plant_status", "date_sprouted", "clone"]
    actions = [copy_plants]


@admin.register(models.PlantMedium)
class PlantMediumAdmin(admin.ModelAdmin):
    list_display = ["medium_name", ]
