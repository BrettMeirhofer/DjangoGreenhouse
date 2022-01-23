from Sensors.views import upload_temp_reading, upload_water_reading, upload_image
from django.urls import path
from django.contrib import admin


class GreenhouseAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('Temp/', upload_temp_reading, name="Temp"),
            path('Water/', upload_water_reading, name="Water"),
            path('upload_image/', upload_image, name="upload_image")
        ]
        return my_urls + urls
