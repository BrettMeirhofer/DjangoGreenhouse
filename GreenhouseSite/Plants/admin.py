from django.contrib import admin
from . import models


admin.site.register(models.Plant)
admin.site.register(models.PlantType)
admin.site.register(models.PlantStatus)
